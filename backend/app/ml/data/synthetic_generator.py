"""
Synthetic Dataset Generator
Genera dataset de entrenamiento usando reglas expertas
"""

import random
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import os


class SyntheticDatasetGenerator:
    """
    Generador de dataset sintetico para el modelo de matching

    Usa reglas expertas para etiquetar ejemplos basandose en:
    - Scores del CV
    - Configuracion institucional
    - Interacciones entre ambos
    """

    def __init__(self, seed: int = 42):
        """
        Args:
            seed: Semilla para reproducibilidad
        """
        random.seed(seed)
        np.random.seed(seed)

        # Distribucion objetivo
        self.target_distribution = {
            'APTO': 0.40,           # 40% - Alta correspondencia
            'CONSIDERADO': 0.35,    # 35% - Media correspondencia
            'NO_APTO': 0.25         # 25% - Baja correspondencia
        }

    def generate_cv_scores(self) -> Dict[str, float]:
        """
        Genera scores aleatorios de un CV sintetico

        Returns:
            Dict con 5 scores [0-1]
        """
        # Distribucion realista (beta distribution)
        # La mayoria de candidatos tiene scores medios-altos

        return {
            'hard_skills': np.random.beta(5, 2),      # Sesgado hacia alto (skill digital comun)
            'soft_skills': np.random.beta(4, 3),      # Distribucion mas uniforme
            'experience': np.random.beta(3, 3),       # Uniforme (experiencia varia mucho)
            'education': random.choice([0.25, 0.45, 0.75, 0.92, 1.0]),  # Categorico
            'languages': np.random.beta(3, 4)         # Sesgado hacia bajo (idiomas extranjeros dificiles)
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
            Dict con anios de experiencia y minimo requerido
        """
        # Experiencia del candidato (0-10 anios, sesgado hacia 2-4 anios)
        total_years = np.random.gamma(3, 1)  # Gamma(3,1) da media ~3 anios
        total_years = min(10.0, total_years)  # Cap en 10 anios

        # Minimo requerido (0-5 anios)
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

        Esta es la LOGICA EXPERTA que el modelo ML aprendera

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

        # === REGLA 2: Penalizacion si no cumple minimo de experiencia ===
        if context['total_years'] < context['min_required']:
            deficit_ratio = context['total_years'] / context['min_required'] if context['min_required'] > 0 else 1.0
            base_score *= (0.5 + 0.5 * deficit_ratio)  # Penalizacion proporcional

        # === REGLA 3: Penalizacion critica si hard skills bajas Y tienen mucho peso ===
        if cv_scores['hard_skills'] < 0.5 and weights['weight_hard'] > 0.3:
            base_score *= 0.7  # Penalizacion del 30%

        # === REGLA 4: Penalizacion critica si soft skills bajas Y tienen mucho peso ===
        if cv_scores['soft_skills'] < 0.4 and weights['weight_soft'] > 0.25:
            base_score *= 0.75  # Penalizacion del 25%

        # === REGLA 5: Bonificacion por educacion maxima ===
        if cv_scores['education'] >= 0.92:  # Maestria o Doctorado
            base_score = min(1.0, base_score * 1.08)  # Bonificacion del 8%

        # === REGLA 6: Bonificacion por perfil muy completo ===
        scores_list = [
            cv_scores['hard_skills'],
            cv_scores['soft_skills'],
            cv_scores['experience'],
            cv_scores['education'],
            cv_scores['languages']
        ]
        if all(s >= 0.7 for s in scores_list):
            base_score = min(1.0, base_score * 1.10)  # Bonificacion del 10%

        # === REGLA 7: Penalizacion si educacion no cumple Y tiene peso alto ===
        if cv_scores['education'] < 0.75 and weights['weight_edu'] > 0.20:
            base_score *= 0.85  # Penalizacion del 15%

        # === REGLA 8: Bonificacion por experiencia muy superior al minimo ===
        if context['delta'] > 2.0:  # 2+ anios por encima del minimo
            base_score = min(1.0, base_score * 1.05)  # Bonificacion del 5%

        # === REGLA 9: Penalizacion si idiomas bajos Y requeridos ===
        if cv_scores['languages'] < 0.5 and weights['weight_lang'] > 0.15:
            base_score *= 0.80  # Penalizacion del 20%

        # === REGLA 10: Sinergia entre hard y soft skills altas ===
        if cv_scores['hard_skills'] > 0.75 and cv_scores['soft_skills'] > 0.75:
            base_score = min(1.0, base_score * 1.07)  # Bonificacion del 7%

        # === REGLA 11: Penalizacion si perfil muy debil en dimension prioritaria ===
        # Mapeo de weight keys a cv_scores keys
        weight_to_score_map = {
            'weight_hard': 'hard_skills',
            'weight_soft': 'soft_skills',
            'weight_exp': 'experience',
            'weight_edu': 'education',
            'weight_lang': 'languages'
        }
        max_weight_dim = max(weights, key=weights.get)
        max_weight_value = weights[max_weight_dim]
        max_weight_score = cv_scores[weight_to_score_map[max_weight_dim]]

        if max_weight_value > 0.35 and max_weight_score < 0.4:
            base_score *= 0.65  # Penalizacion fuerte del 35%

        # === REGLA 12: Bonificacion si sobresale en dimension prioritaria ===
        if max_weight_value > 0.30 and max_weight_score > 0.85:
            base_score = min(1.0, base_score * 1.06)  # Bonificacion del 6%

        # === REGLA 13: Penalizacion por perfil desequilibrado ===
        std_scores = np.std(scores_list)
        if std_scores > 0.35:  # Alta variabilidad (ej: 0.2, 0.9, 0.3, 0.8, 0.1)
            base_score *= 0.90  # Penalizacion del 10%

        # === REGLA 14: Bonificacion por experiencia + educacion alta ===
        if cv_scores['experience'] > 0.7 and cv_scores['education'] >= 0.75:
            base_score = min(1.0, base_score * 1.05)  # Bonificacion del 5%

        # === REGLA 15: Penalizacion extrema si multiples dimensiones criticas fallan ===
        critical_failures = sum([
            cv_scores['hard_skills'] < 0.3,
            cv_scores['soft_skills'] < 0.3,
            cv_scores['experience'] < 0.3,
            cv_scores['education'] < 0.5
        ])

        if critical_failures >= 2:
            base_score *= 0.60  # Penalizacion muy fuerte del 40%

        # === APLICAR RUIDO REALISTA ===
        # Aniadir ruido gaussiano pequenio (+/-3-5%)
        noise = np.random.normal(0, 0.04)
        final_score = base_score + noise

        # Clipear a [0, 1]
        final_score = np.clip(final_score, 0, 1)

        return float(final_score)

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
            n_samples: Numero de ejemplos a generar

        Returns:
            DataFrame con features y labels
        """
        print(f"Generando {n_samples} ejemplos sinteticos...")

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

        # Aniadir clasificacion
        df['classification'] = df['match_score'].apply(self._classify_score)

        print(f"\nDataset generado exitosamente")
        print(f"   Tamanio: {len(df)} ejemplos")
        print(f"   Features: {len(feature_names)}")

        # Mostrar distribucion
        print(f"\nDistribucion de clasificaciones:")
        distribution = df['classification'].value_counts(normalize=True)
        for cls, ratio in distribution.items():
            print(f"   {cls}: {ratio*100:.1f}%")

        return df

    def _classify_score(self, score: float) -> str:
        """Clasifica un score en categorias"""
        if score >= 0.70:
            return 'APTO'
        elif score >= 0.50:
            return 'CONSIDERADO'
        else:
            return 'NO_APTO'

    def save_dataset(self, df: pd.DataFrame, filepath: str = None):
        """
        Guarda dataset a CSV

        Args:
            df: DataFrame a guardar
            filepath: Ruta del archivo (default: training_data/synthetic_dataset.csv)
        """
        if filepath is None:
            # Guardar en la carpeta training_data del modulo
            current_dir = os.path.dirname(__file__)
            filepath = os.path.join(current_dir, 'training_data', 'synthetic_dataset.csv')

        # Crear directorio si no existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        df.to_csv(filepath, index=False)
        print(f"\nDataset guardado en: {filepath}")
        print(f"   Tamanio del archivo: {len(df)} filas x {len(df.columns)} columnas")

        return filepath


def main():
    """Funcion principal para generar dataset"""

    # Crear generador
    generator = SyntheticDatasetGenerator(seed=42)

    # Generar dataset
    df = generator.generate_dataset(n_samples=5000)

    # Guardar
    filepath = generator.save_dataset(df)

    # Estadisticas adicionales
    print(f"\nEstadisticas del dataset:")
    print(f"\n   Match Score:")
    print(f"     Media: {df['match_score'].mean():.3f}")
    print(f"     Mediana: {df['match_score'].median():.3f}")
    print(f"     Std: {df['match_score'].std():.3f}")
    print(f"     Min: {df['match_score'].min():.3f}")
    print(f"     Max: {df['match_score'].max():.3f}")

    return df, filepath


if __name__ == "__main__":
    df, filepath = main()
