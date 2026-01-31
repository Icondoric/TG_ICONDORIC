"""
Model Visualizer - Fase 5
Generacion de visualizaciones para analisis y documento de grado
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import os

# Intentar importar matplotlib y seaborn
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import seaborn as sns
    from sklearn.model_selection import learning_curve
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False


class ModelVisualizer:
    """
    Generador de visualizaciones para el modelo de ML

    Crea graficas profesionales para analisis y documento de grado.
    """

    # Configuracion de estilo
    FIGURE_DPI = 150
    FIGURE_SIZE_STANDARD = (10, 6)
    FIGURE_SIZE_WIDE = (12, 6)
    FIGURE_SIZE_SQUARE = (8, 8)

    # Colores por clasificacion
    COLORS = {
        'APTO': '#2ecc71',        # Verde
        'CONSIDERADO': '#f39c12', # Naranja
        'NO_APTO': '#e74c3c'      # Rojo
    }

    # Umbrales
    THRESHOLD_APTO = 0.70
    THRESHOLD_CONSIDERADO = 0.50

    def __init__(self, style: str = 'whitegrid'):
        """
        Inicializa el visualizador

        Args:
            style: Estilo de seaborn ('whitegrid', 'darkgrid', 'white', 'dark')
        """
        if not PLOTTING_AVAILABLE:
            raise ImportError("matplotlib y seaborn son necesarios para visualizaciones")

        self.style = style
        sns.set_style(style)
        plt.rcParams['figure.dpi'] = self.FIGURE_DPI
        plt.rcParams['savefig.dpi'] = self.FIGURE_DPI
        plt.rcParams['font.size'] = 10

    def _score_to_class(self, score: float) -> str:
        """Convierte score a clasificacion"""
        if score >= self.THRESHOLD_APTO:
            return 'APTO'
        elif score >= self.THRESHOLD_CONSIDERADO:
            return 'CONSIDERADO'
        else:
            return 'NO_APTO'

    def _ensure_dir(self, path: str) -> None:
        """Asegura que el directorio exista"""
        if path:
            os.makedirs(os.path.dirname(path), exist_ok=True)

    def plot_feature_importance(
        self,
        model,
        top_n: int = 15,
        save_path: str = None
    ) -> None:
        """
        Grafica de barras con importancia de features

        Args:
            model: Modelo entrenado con get_coefficients()
            top_n: Numero de features a mostrar
            save_path: Ruta para guardar la grafica
        """
        # Obtener coeficientes
        if hasattr(model, 'get_coefficients'):
            coefficients = model.get_coefficients()
        else:
            raise ValueError("El modelo debe tener metodo get_coefficients()")

        # Ordenar por valor absoluto
        sorted_coeffs = sorted(
            coefficients.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:top_n]

        # Separar nombres y valores
        names = [x[0] for x in sorted_coeffs]
        values = [x[1] for x in sorted_coeffs]

        # Colores segun signo
        colors = ['#2ecc71' if v >= 0 else '#e74c3c' for v in values]

        # Crear figura
        fig, ax = plt.subplots(figsize=self.FIGURE_SIZE_STANDARD)

        # Barras horizontales
        y_pos = np.arange(len(names))
        bars = ax.barh(y_pos, values, color=colors, edgecolor='black', linewidth=0.5)

        # Configurar ejes
        ax.set_yticks(y_pos)
        ax.set_yticklabels(names)
        ax.invert_yaxis()  # Mayor arriba
        ax.set_xlabel('Coeficiente del Modelo')
        ax.set_title('Importancia de Features en el Modelo Ridge')

        # Linea vertical en cero
        ax.axvline(0, color='black', linewidth=0.8)

        # Leyenda
        positive_patch = mpatches.Patch(color='#2ecc71', label='Positivo (aumenta score)')
        negative_patch = mpatches.Patch(color='#e74c3c', label='Negativo (reduce score)')
        ax.legend(handles=[positive_patch, negative_patch], loc='lower right')

        # Grid
        ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()

        # Guardar
        if save_path:
            self._ensure_dir(save_path)
            plt.savefig(save_path, dpi=self.FIGURE_DPI, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"Grafica guardada: {save_path}")

        plt.close()

    def plot_predictions_vs_actual(
        self,
        y_test: np.ndarray,
        y_pred: np.ndarray,
        save_path: str = None
    ) -> None:
        """
        Scatter plot de predicciones vs valores reales

        Args:
            y_test: Valores reales
            y_pred: Valores predichos
            save_path: Ruta para guardar
        """
        from sklearn.metrics import r2_score

        y_test = np.array(y_test)
        y_pred = np.array(y_pred)

        # Clasificaciones para colores
        classes = [self._score_to_class(y) for y in y_test]

        # Crear figura
        fig, ax = plt.subplots(figsize=self.FIGURE_SIZE_STANDARD)

        # Scatter con colores por clase
        for cls in ['NO_APTO', 'CONSIDERADO', 'APTO']:
            mask = np.array(classes) == cls
            ax.scatter(
                y_test[mask], y_pred[mask],
                c=self.COLORS[cls],
                label=cls,
                alpha=0.6,
                edgecolors='white',
                linewidth=0.5,
                s=50
            )

        # Linea diagonal (prediccion perfecta)
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        ax.plot(
            [min_val, max_val], [min_val, max_val],
            'r--', linewidth=2, label='Prediccion perfecta'
        )

        # Calcular R2
        r2 = r2_score(y_test, y_pred)

        # Configurar
        ax.set_xlabel('Match Score Real')
        ax.set_ylabel('Match Score Predicho')
        ax.set_title(f'Predicciones vs Valores Reales (R2 = {r2:.4f})')
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3)

        # Limites
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)

        plt.tight_layout()

        if save_path:
            self._ensure_dir(save_path)
            plt.savefig(save_path, dpi=self.FIGURE_DPI, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"Grafica guardada: {save_path}")

        plt.close()

    def plot_residuals_distribution(
        self,
        y_test: np.ndarray,
        y_pred: np.ndarray,
        save_path: str = None
    ) -> None:
        """
        Distribucion de residuos (2 subplots)

        Args:
            y_test: Valores reales
            y_pred: Valores predichos
            save_path: Ruta para guardar
        """
        y_test = np.array(y_test)
        y_pred = np.array(y_pred)
        residuals = y_test - y_pred

        # Crear figura con 2 subplots
        fig, axes = plt.subplots(1, 2, figsize=self.FIGURE_SIZE_WIDE)

        # Subplot 1: Histograma de residuos
        ax1 = axes[0]
        ax1.hist(residuals, bins=50, color='#3498db', edgecolor='black',
                alpha=0.7, density=True)
        ax1.axvline(0, color='red', linestyle='--', linewidth=2, label='Cero')
        ax1.axvline(residuals.mean(), color='green', linestyle='-', linewidth=2,
                   label=f'Media ({residuals.mean():.4f})')
        ax1.set_xlabel('Residuos (Real - Predicho)')
        ax1.set_ylabel('Densidad')
        ax1.set_title('Distribucion de Residuos')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Subplot 2: Residuos vs Predicciones
        ax2 = axes[1]
        ax2.scatter(y_pred, residuals, alpha=0.5, color='#3498db',
                   edgecolors='white', linewidth=0.3, s=30)
        ax2.axhline(0, color='red', linestyle='--', linewidth=2)

        # Lineas de +/- 2 std
        std = residuals.std()
        ax2.axhline(2*std, color='orange', linestyle=':', linewidth=1.5,
                   label=f'+2 std ({2*std:.3f})')
        ax2.axhline(-2*std, color='orange', linestyle=':', linewidth=1.5,
                   label=f'-2 std ({-2*std:.3f})')

        ax2.set_xlabel('Match Score Predicho')
        ax2.set_ylabel('Residuos')
        ax2.set_title('Residuos vs Predicciones')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            self._ensure_dir(save_path)
            plt.savefig(save_path, dpi=self.FIGURE_DPI, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"Grafica guardada: {save_path}")

        plt.close()

    def plot_confusion_matrix(
        self,
        y_test: np.ndarray,
        y_pred: np.ndarray,
        save_path: str = None
    ) -> None:
        """
        Matriz de confusion 3x3

        Args:
            y_test: Valores reales (scores)
            y_pred: Valores predichos (scores)
            save_path: Ruta para guardar
        """
        from sklearn.metrics import confusion_matrix

        # Convertir a clases
        y_test_class = [self._score_to_class(y) for y in y_test]
        y_pred_class = [self._score_to_class(y) for y in y_pred]

        # Calcular matriz
        class_names = ['NO_APTO', 'CONSIDERADO', 'APTO']
        cm = confusion_matrix(y_test_class, y_pred_class, labels=class_names)

        # Calcular porcentajes
        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        # Crear figura
        fig, ax = plt.subplots(figsize=self.FIGURE_SIZE_SQUARE)

        # Heatmap
        im = ax.imshow(cm, interpolation='nearest', cmap='Blues')
        ax.figure.colorbar(im, ax=ax, label='Cantidad')

        # Etiquetas
        ax.set(
            xticks=np.arange(cm.shape[1]),
            yticks=np.arange(cm.shape[0]),
            xticklabels=class_names,
            yticklabels=class_names,
            ylabel='Clase Real',
            xlabel='Clase Predicha',
            title='Matriz de Confusion'
        )

        # Rotar etiquetas del eje x
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # Agregar valores en cada celda
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                value = cm[i, j]
                pct = cm_normalized[i, j] * 100
                ax.text(
                    j, i,
                    f'{value}\n({pct:.1f}%)',
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black",
                    fontsize=10
                )

        plt.tight_layout()

        if save_path:
            self._ensure_dir(save_path)
            plt.savefig(save_path, dpi=self.FIGURE_DPI, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"Grafica guardada: {save_path}")

        plt.close()

    def plot_score_distribution_by_class(
        self,
        y_test: np.ndarray,
        y_pred: np.ndarray,
        save_path: str = None
    ) -> None:
        """
        Boxplots de scores predichos por clase real

        Args:
            y_test: Valores reales
            y_pred: Valores predichos
            save_path: Ruta para guardar
        """
        import pandas as pd

        y_test = np.array(y_test)
        y_pred = np.array(y_pred)

        # Crear DataFrame
        classes = [self._score_to_class(y) for y in y_test]
        df = pd.DataFrame({
            'Score Predicho': y_pred,
            'Clase Real': classes
        })

        # Ordenar clases
        class_order = ['NO_APTO', 'CONSIDERADO', 'APTO']

        # Crear figura
        fig, ax = plt.subplots(figsize=self.FIGURE_SIZE_STANDARD)

        # Boxplot
        bp = ax.boxplot(
            [df[df['Clase Real'] == c]['Score Predicho'].values for c in class_order],
            labels=class_order,
            patch_artist=True,
            showmeans=True,
            meanline=True
        )

        # Colores
        for patch, color in zip(bp['boxes'], [self.COLORS[c] for c in class_order]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        # Lineas de umbral
        ax.axhline(self.THRESHOLD_APTO, color='green', linestyle='--',
                  linewidth=2, label=f'Umbral APTO ({self.THRESHOLD_APTO})')
        ax.axhline(self.THRESHOLD_CONSIDERADO, color='orange', linestyle='--',
                  linewidth=2, label=f'Umbral CONSIDERADO ({self.THRESHOLD_CONSIDERADO})')

        # Configurar
        ax.set_xlabel('Clase Real')
        ax.set_ylabel('Score Predicho')
        ax.set_title('Distribucion de Scores Predichos por Clase Real')
        ax.legend(loc='upper left')
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(-0.05, 1.05)

        plt.tight_layout()

        if save_path:
            self._ensure_dir(save_path)
            plt.savefig(save_path, dpi=self.FIGURE_DPI, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"Grafica guardada: {save_path}")

        plt.close()

    def plot_cv_scores_distribution(
        self,
        cv_scores: List[float],
        save_path: str = None
    ) -> None:
        """
        Distribucion de scores de Cross-Validation

        Args:
            cv_scores: Lista de scores de cada fold
            save_path: Ruta para guardar
        """
        cv_scores = np.array(cv_scores)

        # Crear figura
        fig, ax = plt.subplots(figsize=self.FIGURE_SIZE_STANDARD)

        # Barras para cada fold
        folds = range(1, len(cv_scores) + 1)
        colors = ['#3498db' if s >= cv_scores.mean() else '#e74c3c' for s in cv_scores]

        bars = ax.bar(folds, cv_scores, color=colors, edgecolor='black', linewidth=0.5)

        # Linea de media
        mean = cv_scores.mean()
        std = cv_scores.std()
        ax.axhline(mean, color='green', linestyle='-', linewidth=2,
                  label=f'Media: {mean:.4f}')
        ax.axhline(mean + std, color='green', linestyle=':', linewidth=1.5,
                  label=f'+1 Std: {mean+std:.4f}')
        ax.axhline(mean - std, color='green', linestyle=':', linewidth=1.5,
                  label=f'-1 Std: {mean-std:.4f}')

        # Configurar
        ax.set_xlabel('Fold de Cross-Validation')
        ax.set_ylabel('R2 Score')
        ax.set_title(f'Scores de Cross-Validation (5-Fold)\nMedia: {mean:.4f} +/- {std:.4f}')
        ax.set_xticks(folds)
        ax.legend(loc='lower right')
        ax.grid(axis='y', alpha=0.3)

        # Agregar valores sobre barras
        for bar, score in zip(bars, cv_scores):
            ax.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.01,
                f'{score:.3f}',
                ha='center', va='bottom',
                fontsize=9
            )

        plt.tight_layout()

        if save_path:
            self._ensure_dir(save_path)
            plt.savefig(save_path, dpi=self.FIGURE_DPI, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"Grafica guardada: {save_path}")

        plt.close()

    def plot_learning_curve(
        self,
        model,
        X: np.ndarray,
        y: np.ndarray,
        cv: int = 5,
        save_path: str = None
    ) -> None:
        """
        Curva de aprendizaje del modelo

        Args:
            model: Modelo sklearn (no el wrapper)
            X: Features completos
            y: Target completo
            cv: Numero de folds
            save_path: Ruta para guardar
        """
        # Obtener modelo sklearn subyacente
        if hasattr(model, 'model'):
            sklearn_model = model.model
        else:
            sklearn_model = model

        # Calcular curva de aprendizaje
        train_sizes = np.linspace(0.1, 1.0, 10)

        train_sizes_abs, train_scores, val_scores = learning_curve(
            sklearn_model, X, y,
            train_sizes=train_sizes,
            cv=cv,
            scoring='r2',
            n_jobs=-1
        )

        # Calcular medias y std
        train_mean = train_scores.mean(axis=1)
        train_std = train_scores.std(axis=1)
        val_mean = val_scores.mean(axis=1)
        val_std = val_scores.std(axis=1)

        # Crear figura
        fig, ax = plt.subplots(figsize=self.FIGURE_SIZE_STANDARD)

        # Plot train scores
        ax.fill_between(
            train_sizes_abs,
            train_mean - train_std,
            train_mean + train_std,
            alpha=0.2, color='blue'
        )
        ax.plot(
            train_sizes_abs, train_mean,
            'o-', color='blue', linewidth=2,
            label='Score de Entrenamiento'
        )

        # Plot validation scores
        ax.fill_between(
            train_sizes_abs,
            val_mean - val_std,
            val_mean + val_std,
            alpha=0.2, color='green'
        )
        ax.plot(
            train_sizes_abs, val_mean,
            'o-', color='green', linewidth=2,
            label='Score de Validacion'
        )

        # Configurar
        ax.set_xlabel('Tamano del Training Set')
        ax.set_ylabel('R2 Score')
        ax.set_title('Curva de Aprendizaje del Modelo Ridge')
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3)

        # Analisis de over/underfitting
        gap = train_mean[-1] - val_mean[-1]
        if gap > 0.1:
            diagnosis = "Posible Overfitting"
        elif val_mean[-1] < 0.6:
            diagnosis = "Posible Underfitting"
        else:
            diagnosis = "Buen ajuste"

        ax.text(
            0.02, 0.02,
            f'Diagnostico: {diagnosis}\nGap final: {gap:.4f}',
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )

        plt.tight_layout()

        if save_path:
            self._ensure_dir(save_path)
            plt.savefig(save_path, dpi=self.FIGURE_DPI, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"Grafica guardada: {save_path}")

        plt.close()

    def plot_coefficients_heatmap(
        self,
        model,
        save_path: str = None
    ) -> None:
        """
        Heatmap de coeficientes del modelo

        Args:
            model: Modelo con get_coefficients()
            save_path: Ruta para guardar
        """
        coefficients = model.get_coefficients()

        # Organizar en grupos
        groups = {
            'CV Scores': ['hard_skills_score', 'soft_skills_score', 'experience_score',
                         'education_score', 'languages_score'],
            'Pesos Inst.': ['inst_weight_hard', 'inst_weight_soft', 'inst_weight_exp',
                          'inst_weight_edu', 'inst_weight_lang'],
            'Interacciones': ['interaction_hard', 'interaction_soft', 'interaction_exp',
                            'interaction_edu', 'interaction_lang'],
            'Contexto': ['total_experience_years', 'min_required_years', 'experience_delta']
        }

        # Crear matriz
        group_names = list(groups.keys())
        max_features = max(len(v) for v in groups.values())

        matrix = np.full((len(groups), max_features), np.nan)

        for i, (group, features) in enumerate(groups.items()):
            for j, feat in enumerate(features):
                if feat in coefficients:
                    matrix[i, j] = coefficients[feat]

        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 6))

        # Heatmap
        im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto', vmin=-0.5, vmax=0.5)

        # Colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.set_label('Coeficiente')

        # Etiquetas
        ax.set_yticks(range(len(group_names)))
        ax.set_yticklabels(group_names)
        ax.set_xticks(range(max_features))

        # Agregar valores
        for i, (group, features) in enumerate(groups.items()):
            for j, feat in enumerate(features):
                if feat in coefficients:
                    val = coefficients[feat]
                    color = 'white' if abs(val) > 0.3 else 'black'
                    ax.text(j, i, f'{val:.3f}', ha='center', va='center',
                           color=color, fontsize=8)
                    ax.text(j, i + 0.35, feat.replace('_', '\n')[:15],
                           ha='center', va='top', fontsize=6, color='gray')

        ax.set_title('Mapa de Coeficientes del Modelo Ridge')

        plt.tight_layout()

        if save_path:
            self._ensure_dir(save_path)
            plt.savefig(save_path, dpi=self.FIGURE_DPI, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"Grafica guardada: {save_path}")

        plt.close()

    def create_full_evaluation_report(
        self,
        model,
        X_test: np.ndarray,
        y_test: np.ndarray,
        feature_names: List[str],
        cv_scores: List[float] = None,
        X_full: np.ndarray = None,
        y_full: np.ndarray = None,
        output_dir: str = 'visualizations/'
    ) -> Dict[str, str]:
        """
        Genera todas las visualizaciones en un directorio

        Args:
            model: Modelo entrenado
            X_test: Features de test
            y_test: Target de test
            feature_names: Nombres de features
            cv_scores: Scores de Cross-Validation (opcional)
            X_full: Dataset completo para curva de aprendizaje (opcional)
            y_full: Target completo para curva de aprendizaje (opcional)
            output_dir: Directorio de salida

        Returns:
            Dict con rutas de archivos generados
        """
        # Crear directorio
        os.makedirs(output_dir, exist_ok=True)

        # Obtener predicciones
        y_pred = model.predict(X_test)

        # Dict para almacenar rutas
        generated_files = {}

        # 1. Feature Importance
        path = os.path.join(output_dir, 'feature_importance.png')
        self.plot_feature_importance(model, top_n=15, save_path=path)
        generated_files['feature_importance'] = path

        # 2. Predictions vs Actual
        path = os.path.join(output_dir, 'predictions_vs_actual.png')
        self.plot_predictions_vs_actual(y_test, y_pred, save_path=path)
        generated_files['predictions_vs_actual'] = path

        # 3. Residuals Distribution
        path = os.path.join(output_dir, 'residuals_distribution.png')
        self.plot_residuals_distribution(y_test, y_pred, save_path=path)
        generated_files['residuals_distribution'] = path

        # 4. Confusion Matrix
        path = os.path.join(output_dir, 'confusion_matrix.png')
        self.plot_confusion_matrix(y_test, y_pred, save_path=path)
        generated_files['confusion_matrix'] = path

        # 5. Score Distribution by Class
        path = os.path.join(output_dir, 'score_distribution_by_class.png')
        self.plot_score_distribution_by_class(y_test, y_pred, save_path=path)
        generated_files['score_distribution_by_class'] = path

        # 6. CV Scores Distribution (si disponible)
        if cv_scores is not None:
            path = os.path.join(output_dir, 'cv_scores_distribution.png')
            self.plot_cv_scores_distribution(cv_scores, save_path=path)
            generated_files['cv_scores_distribution'] = path

        # 7. Learning Curve (si dataset completo disponible)
        if X_full is not None and y_full is not None:
            path = os.path.join(output_dir, 'learning_curve.png')
            self.plot_learning_curve(model, X_full, y_full, cv=5, save_path=path)
            generated_files['learning_curve'] = path

        # 8. Coefficients Heatmap
        path = os.path.join(output_dir, 'coefficients_heatmap.png')
        self.plot_coefficients_heatmap(model, save_path=path)
        generated_files['coefficients_heatmap'] = path

        print(f"\nVisualizaciones generadas en: {output_dir}")
        print(f"Total de graficas: {len(generated_files)}")

        return generated_files
