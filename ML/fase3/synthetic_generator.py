"""
Synthetic Dataset Generator
Genera dataset de entrenamiento usando reglas expertas
"""

import random
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import json


class SyntheticDatasetGenerator:
    """
    Generador de dataset sintético para el modelo de matching
    
    Usa reglas expertas para etiquetar ejemplos basándose en:
    - Scores del CV
    - Configuración institucional
    - Interacciones entre ambos
    """
    
    def __init__(self, seed: int = 42):
        """
        Args:
            seed: Semilla para reproducibilidad
        """
        random.seed(seed)
        np.random.seed(seed)
        
        # Distribución objetivo
        self.target_distribution = {
            'APTO': 0.40,           # 40% - Alta correspondencia
            'CONSIDERADO': 0.35,    # 35% - Media correspondencia
            'NO_APTO': 0.25         # 25% - Baja correspondencia
        }
    
    def generate_cv_scores(self) -> Dict[str, float]:
        """
        Genera scores aleatorios de un CV sintético
        
        Returns:
            Dict con 5 scores [0-1]
        """
        # Distribución realista (beta distribution)
        # La mayoría de candidatos tiene scores medios-altos
        
        return {
            'hard_skills': np.random.beta(5, 2),      # Sesgado hacia alto (skill digital común)
            'soft_skills': np.random.beta(4, 3),      # Distribución más uniforme
            'experience': np.random.beta(3, 3),       # Uniforme (experiencia varía mucho)
            'education': random.choice([0.25, 0.45, 0.75, 0.92, 1.0]),  # Categórico
            'languages': np.random.beta(3, 4)         # Sesgado hacia bajo (idiomas extranjeros difíciles)
        }
    
    def generate_institutional_weights(self) -> Dict[str, float]:
        """
        Genera pesos institucionales aleatorios que sumen 1.0
        
        Returns:
            Dict con 5 pesos [0-1] que suman 1.0
        """
        # Generar 5 valores aleatorios
        weights = np.random.dirichlet([2, 2, 2, 2, 2])  # Dirichlet garantiza suma = 1
        
        return {
            'weight_hard': float(weights[0]),
            'weight_soft': float(weights[1]),
            'weight_exp': float(weights[2]),
            'weight_edu': float(weights[3]),
            'weight_lang': float(weights[4])
        }
    
    def generate_context_features(self) -> Dict[str, float]:
        """
        Genera features de contexto (experiencia absoluta)
        
        Returns:
            Dict con años de experiencia y mínimo requerido
        """
        # Experiencia del candidato (0-10 años, sesgado hacia 2-4 años)
        total_years = np.random.gamma(3, 1)  # Gamma(3,1) da media ~3 años
        total_years = min(10.0, total_years)  # Cap en 10 años
        
        # Mínimo requerido (0-5 años)
        min_required = random.uniform(0, 5)
        
        return {
            'total_years': total_years,
            'min_required': min_required,
            'delta': total_years - min_required
        }
    
    def apply_expert_rules(
        self,
        cv_scores: Dict[str, float],
        weights: Dict[str, float],
        context: Dict[str, float]
    ) -> float:
        """
        Aplica reglas expertas para calcular el score "verdadero"
        
        Esta es la LÓGICA EXPERTA que el modelo ML aprenderá
        
        Args:
            cv_scores: Scores del CV
            weights: Pesos institucionales
            context: Features de contexto
        
        Returns:
            Score de matching [0-1]
        """
        
        # === REGLA 1: Score base ponderado ===
        base_score = (
            cv_scores['hard_skills'] * weights['weight_hard'] +
            cv_scores['soft_skills'] * weights['weight_soft'] +
            cv_scores['experience'] * weights['weight_exp'] +
            cv_scores['education'] * weights['weight_edu'] +
            cv_scores['languages'] * weights['weight_lang']
        )
        
        # === REGLA 2: Penalización si no cumple mínimo de experiencia ===
        if context['total_years'] < context['min_required']:
            deficit_ratio = context['total_years'] / context['min_required'] if context['min_required'] > 0 else 1.0
            base_score *= (0.5 + 0.5 * deficit_ratio)  # Penalización proporcional
        
        # === REGLA 3: Penalización crítica si hard skills bajas Y tienen mucho peso ===
        if cv_scores['hard_skills'] < 0.5 and weights['weight_hard'] > 0.3:
            base_score *= 0.7  # Penalización del 30%
        
        # === REGLA 4: Penalización crítica si soft skills bajas Y tienen mucho peso ===
        if cv_scores['soft_skills'] < 0.4 and weights['weight_soft'] > 0.25:
            base_score *= 0.75  # Penalización del 25%
        
        # === REGLA 5: Bonificación por educación máxima ===
        if cv_scores['education'] >= 0.92:  # Maestría o Doctorado
            base_score = min(1.0, base_score * 1.08)  # Bonificación del 8%
        
        # === REGLA 6: Bonificación por perfil muy completo ===
        scores_list = [
            cv_scores['hard_skills'],
            cv_scores['soft_skills'],
            cv_scores['experience'],
            cv_scores['education'],
            cv_scores['languages']
        ]
        if all(s >= 0.7 for s in scores_list):
            base_score = min(1.0, base_score * 1.10)  # Bonificación del 10%
        
        # === REGLA 7: Penalización si educación no cumple Y tiene peso alto ===
        if cv_scores['education'] < 0.75 and weights['weight_edu'] > 0.20:
            base_score *= 0.85  # Penalización del 15%
        
        # === REGLA 8: Bonificación por experiencia muy superior al mínimo ===
        if context['delta'] > 2.0:  # 2+ años por encima del mínimo
            base_score = min(1.0, base_score * 1.05)  # Bonificación del 5%
        
        # === REGLA 9: Penalización si idiomas bajos Y requeridos ===
        if cv_scores['languages'] < 0.5 and weights['weight_lang'] > 0.15:
            base_score *= 0.80  # Penalización del 20%
        
        # === REGLA 10: Sinergia entre hard y soft skills altas ===
        if cv_scores['hard_skills'] > 0.75 and cv_scores['soft_skills'] > 0.75:
            base_score = min(1.0, base_score * 1.07)  # Bonificación del 7%
        
        # === REGLA 11: Penalización si perfil muy débil en dimensión prioritaria ===
        max_weight_dim = max(weights, key=weights.get)
        max_weight_value = weights[max_weight_dim]
        max_weight_score = cv_scores[max_weight_dim.replace('weight_', '')]
        
        if max_weight_value > 0.35 and max_weight_score < 0.4:
            base_score *= 0.65  # Penalización fuerte del 35%
        
        # === REGLA 12: Bonificación si sobresale en dimensión prioritaria ===
        if max_weight_value > 0.30 and max_weight_score > 0.85:
            base_score = min(1.0, base_score * 1.06)  # Bonificación del 6%
        
        # === REGLA 13: Penalización por perfil desequilibrado ===
        std_scores = np.std(scores_list)
        if std_scores > 0.35:  # Alta variabilidad (ej: 0.2, 0.9, 0.3, 0.8, 0.1)
            base_score *= 0.90  # Penalización del 10%
        
        # === REGLA 14: Bonificación por experiencia + educación alta ===
        if cv_scores['experience'] > 0.7 and cv_scores['education'] >= 0.75:
            base_score = min(1.0, base_score * 1.05)  # Bonificación del 5%
        
        # === REGLA 15: Penalización extrema si múltiples dimensiones críticas fallan ===
        critical_failures = sum([
            cv_scores['hard_skills'] < 0.3,
            cv_scores['soft_skills'] < 0.3,
            cv_scores['experience'] < 0.3,
            cv_scores['education'] < 0.5
        ])
        
        if critical_failures >= 2:
            base_score *= 0.60  # Penalización muy fuerte del 40%
        
        # === APLICAR RUIDO REALISTA ===
        # Añadir ruido gaussiano pequeño (±3-5%)
        noise = np.random.normal(0, 0.04)
        final_score = base_score + noise
        
        # Clipear a [0, 1]
        final_score = np.clip(final_score, 0, 1)
        
        return final_score
    
    def generate_sample(self) -> Tuple[List[float], float]:
        """
        Genera UN ejemplo completo (features + label)
        
        Returns:
            Tupla (feature_vector, score)
        """
        # Generar componentes
        cv_scores = self.generate_cv_scores()
        weights = self.generate_institutional_weights()
        context = self.generate_context_features()
        
        # Aplicar reglas expertas para obtener label
        true_score = self.apply_expert_rules(cv_scores, weights, context)
        
        # Construir feature vector (igual que en feature_extractor.py)
        feature_vector = [
            # CV Scores (5)
            cv_scores['hard_skills'],
            cv_scores['soft_skills'],
            cv_scores['experience'],
            cv_scores['education'],
            cv_scores['languages'],
            
            # Institutional weights (5)
            weights['weight_hard'],
            weights['weight_soft'],
            weights['weight_exp'],
            weights['weight_edu'],
            weights['weight_lang'],
            
            # Interaction features (5)
            cv_scores['hard_skills'] * weights['weight_hard'],
            cv_scores['soft_skills'] * weights['weight_soft'],
            cv_scores['experience'] * weights['weight_exp'],
            cv_scores['education'] * weights['weight_edu'],
            cv_scores['languages'] * weights['weight_lang'],
            
            # Context features (3)
            context['total_years'],
            context['min_required'],
            context['delta']
        ]
        
        return feature_vector, true_score
    
    def generate_dataset(self, n_samples: int = 5000) -> pd.DataFrame:
        """
        Genera dataset completo
        
        Args:
            n_samples: Número de ejemplos a generar
        
        Returns:
            DataFrame con features y labels
        """
        print(f"Generando {n_samples} ejemplos sintéticos...")
        
        X = []
        y = []
        
        for i in range(n_samples):
            if (i + 1) % 1000 == 0:
                print(f"  Generados: {i + 1}/{n_samples}")
            
            feature_vector, score = self.generate_sample()
            X.append(feature_vector)
            y.append(score)
        
        # Crear DataFrame
        feature_names = [
            'hard_skills_score', 'soft_skills_score', 'experience_score',
            'education_score', 'languages_score',
            'inst_weight_hard', 'inst_weight_soft', 'inst_weight_exp',
            'inst_weight_edu', 'inst_weight_lang',
            'interaction_hard', 'interaction_soft', 'interaction_exp',
            'interaction_edu', 'interaction_lang',
            'total_experience_years', 'min_required_years', 'experience_delta'
        ]
        
        df = pd.DataFrame(X, columns=feature_names)
        df['match_score'] = y
        
        # Añadir clasificación
        df['classification'] = df['match_score'].apply(self._classify_score)
        
        print(f"\n✅ Dataset generado exitosamente")
        print(f"   Tamaño: {len(df)} ejemplos")
        print(f"   Features: {len(feature_names)}")
        
        # Mostrar distribución
        print(f"\n📊 Distribución de clasificaciones:")
        distribution = df['classification'].value_counts(normalize=True)
        for cls, ratio in distribution.items():
            print(f"   {cls}: {ratio*100:.1f}%")
        
        return df
    
    def _classify_score(self, score: float) -> str:
        """Clasifica un score en categorías"""
        if score >= 0.70:
            return 'APTO'
        elif score >= 0.50:
            return 'CONSIDERADO'
        else:
            return 'NO_APTO'
    
    def save_dataset(self, df: pd.DataFrame, filepath: str = 'synthetic_dataset.csv'):
        """
        Guarda dataset a CSV
        
        Args:
            df: DataFrame a guardar
            filepath: Ruta del archivo
        """
        df.to_csv(filepath, index=False)
        print(f"\n💾 Dataset guardado en: {filepath}")
        print(f"   Tamaño del archivo: {len(df)} filas × {len(df.columns)} columnas")


def main():
    """Función principal para generar dataset"""
    
    # Crear generador
    generator = SyntheticDatasetGenerator(seed=42)
    
    # Generar dataset
    df = generator.generate_dataset(n_samples=5000)
    
    # Guardar
    generator.save_dataset(df, filepath='synthetic_dataset.csv')
    
    # Estadísticas adicionales
    print(f"\n📈 Estadísticas del dataset:")
    print(f"\n   Match Score:")
    print(f"     Media: {df['match_score'].mean():.3f}")
    print(f"     Mediana: {df['match_score'].median():.3f}")
    print(f"     Std: {df['match_score'].std():.3f}")
    print(f"     Min: {df['match_score'].min():.3f}")
    print(f"     Max: {df['match_score'].max():.3f}")
    
    return df


if __name__ == "__main__":
    df = main()
