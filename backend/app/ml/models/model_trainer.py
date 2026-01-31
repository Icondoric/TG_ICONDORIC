"""
Model Trainer
Entrenamiento del modelo con validacion cruzada y grid search
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Dict, Tuple, Optional
import os

from .ridge_model import InstitutionalMatchModel

# Intentar importar matplotlib (opcional)
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False


class ModelTrainer:
    """
    Entrena y evalua el modelo de matching institucional
    """

    def __init__(self, random_state: int = 42):
        """
        Args:
            random_state: Semilla para reproducibilidad
        """
        self.random_state = random_state
        self.best_model = None
        self.best_params = None
        self.training_history = {}

    def load_dataset(self, filepath: str) -> Tuple[np.ndarray, np.ndarray, list]:
        """
        Carga dataset desde CSV

        Args:
            filepath: Ruta del archivo CSV

        Returns:
            Tupla (X, y, feature_names)
        """
        print(f"Cargando dataset desde: {filepath}")
        df = pd.read_csv(filepath)

        # Separar features y target
        feature_cols = [col for col in df.columns if col not in ['match_score', 'classification']]

        X = df[feature_cols].values
        y = df['match_score'].values
        feature_names = feature_cols

        print(f"Dataset cargado:")
        print(f"   Ejemplos: {len(X)}")
        print(f"   Features: {len(feature_names)}")
        print(f"   Target: match_score")

        return X, y, feature_names

    def train_test_split_data(
        self,
        X: np.ndarray,
        y: np.ndarray,
        test_size: float = 0.2
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Divide dataset en train/test

        Args:
            X: Features
            y: Target
            test_size: Proporcion del test set

        Returns:
            Tupla (X_train, X_test, y_train, y_test)
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=self.random_state,
            shuffle=True
        )

        print(f"\nSplit de datos:")
        print(f"   Train: {len(X_train)} ejemplos ({(1-test_size)*100:.0f}%)")
        print(f"   Test:  {len(X_test)} ejemplos ({test_size*100:.0f}%)")

        return X_train, X_test, y_train, y_test

    def train_with_cross_validation(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        alpha: float = 1.0,
        cv_folds: int = 5,
        feature_names: list = None
    ) -> InstitutionalMatchModel:
        """
        Entrena modelo con validacion cruzada

        Args:
            X_train: Features de entrenamiento
            y_train: Target de entrenamiento
            alpha: Parametro de regularizacion
            cv_folds: Numero de folds para cross-validation
            feature_names: Nombres de features

        Returns:
            Modelo entrenado
        """
        print(f"\nEntrenando con validacion cruzada ({cv_folds}-fold)...")
        print(f"   Alpha: {alpha}")

        # Crear modelo
        model = InstitutionalMatchModel(alpha=alpha, normalize=True)

        # Cross-validation
        cv_scores = cross_val_score(
            model.model,
            X_train,
            y_train,
            cv=cv_folds,
            scoring='r2',
            n_jobs=-1
        )

        print(f"\nResultados de Cross-Validation:")
        print(f"   R2 scores: {cv_scores}")
        print(f"   R2 medio: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")

        # Entrenar modelo final con todos los datos de train
        model.fit(X_train, y_train, feature_names=feature_names)

        # Guardar metricas de CV
        self.training_history['cv_r2_mean'] = cv_scores.mean()
        self.training_history['cv_r2_std'] = cv_scores.std()
        self.training_history['cv_scores'] = cv_scores.tolist()

        return model

    def grid_search_alpha(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        alphas: list = None,
        cv_folds: int = 5
    ) -> Dict:
        """
        Encuentra el mejor alpha usando Grid Search

        Args:
            X_train: Features de entrenamiento
            y_train: Target de entrenamiento
            alphas: Lista de alphas a probar
            cv_folds: Numero de folds

        Returns:
            Dict con resultados del grid search
        """
        if alphas is None:
            # Valores por defecto: rango logaritmico
            alphas = [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0]

        print(f"\nGrid Search de Alpha...")
        print(f"   Valores a probar: {alphas}")
        print(f"   Cross-validation: {cv_folds}-fold")

        # Grid Search
        from sklearn.linear_model import Ridge

        grid_search = GridSearchCV(
            Ridge(),
            param_grid={'alpha': alphas},
            cv=cv_folds,
            scoring='r2',
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(X_train, y_train)

        # Resultados
        results = {
            'best_alpha': grid_search.best_params_['alpha'],
            'best_score': grid_search.best_score_,
            'all_results': pd.DataFrame(grid_search.cv_results_)
        }

        print(f"\nMejor Alpha encontrado: {results['best_alpha']}")
        print(f"   R2 Score: {results['best_score']:.4f}")

        # Guardar para referencia
        self.best_params = results

        return results

    def evaluate_model(
        self,
        model: InstitutionalMatchModel,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> Dict[str, float]:
        """
        Evalua modelo en test set

        Args:
            model: Modelo entrenado
            X_test: Features de test
            y_test: Target de test

        Returns:
            Dict con metricas
        """
        print(f"\nEvaluando en Test Set...")

        # Predicciones
        y_pred = model.predict(X_test)

        # Calcular metricas
        metrics = {
            'r2_score': r2_score(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred)
        }

        print(f"\n   Metricas en Test:")
        print(f"   R2 Score: {metrics['r2_score']:.4f}")
        print(f"   MSE:      {metrics['mse']:.4f}")
        print(f"   RMSE:     {metrics['rmse']:.4f}")
        print(f"   MAE:      {metrics['mae']:.4f}")

        # Clasificacion
        y_test_class = np.array([self._classify(s) for s in y_test])
        y_pred_class = np.array([self._classify(s) for s in y_pred])

        accuracy = (y_test_class == y_pred_class).mean()
        print(f"   Accuracy (clasificacion): {accuracy:.4f}")

        metrics['classification_accuracy'] = accuracy

        # Guardar
        self.training_history['test_metrics'] = metrics

        return metrics

    def _classify(self, score: float) -> str:
        """Clasifica un score"""
        if score >= 0.70:
            return 'APTO'
        elif score >= 0.50:
            return 'CONSIDERADO'
        else:
            return 'NO_APTO'

    def plot_predictions(
        self,
        model: InstitutionalMatchModel,
        X_test: np.ndarray,
        y_test: np.ndarray,
        save_path: Optional[str] = None
    ):
        """
        Grafica predicciones vs valores reales

        Args:
            model: Modelo entrenado
            X_test: Features de test
            y_test: Target de test
            save_path: Ruta para guardar grafica
        """
        if not PLOTTING_AVAILABLE:
            print("Visualizaciones no disponibles (matplotlib no instalado)")
            return

        y_pred = model.predict(X_test)

        plt.figure(figsize=(10, 6))

        # Scatter plot
        plt.scatter(y_test, y_pred, alpha=0.5, edgecolors='k', linewidth=0.5)

        # Linea ideal (y = x)
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Prediccion perfecta')

        plt.xlabel('Match Score Real')
        plt.ylabel('Match Score Predicho')
        plt.title(f'Predicciones vs Valores Reales (R2={r2_score(y_test, y_pred):.3f})')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"   Grafica guardada: {save_path}")

        plt.close()

    def plot_residuals(
        self,
        model: InstitutionalMatchModel,
        X_test: np.ndarray,
        y_test: np.ndarray,
        save_path: Optional[str] = None
    ):
        """
        Grafica distribucion de residuos

        Args:
            model: Modelo entrenado
            X_test: Features de test
            y_test: Target de test
            save_path: Ruta para guardar grafica
        """
        if not PLOTTING_AVAILABLE:
            print("Visualizaciones no disponibles (matplotlib no instalado)")
            return

        y_pred = model.predict(X_test)
        residuals = y_test - y_pred

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Histograma de residuos
        axes[0].hist(residuals, bins=50, edgecolor='black', alpha=0.7)
        axes[0].axvline(0, color='red', linestyle='--', linewidth=2)
        axes[0].set_xlabel('Residuos (Real - Predicho)')
        axes[0].set_ylabel('Frecuencia')
        axes[0].set_title('Distribucion de Residuos')
        axes[0].grid(True, alpha=0.3)

        # Residuos vs predicciones
        axes[1].scatter(y_pred, residuals, alpha=0.5, edgecolors='k', linewidth=0.5)
        axes[1].axhline(0, color='red', linestyle='--', linewidth=2)
        axes[1].set_xlabel('Match Score Predicho')
        axes[1].set_ylabel('Residuos')
        axes[1].set_title('Residuos vs Predicciones')
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"   Grafica guardada: {save_path}")

        plt.close()

    def full_training_pipeline(
        self,
        dataset_path: str,
        output_model_path: str,
        visualizations_dir: str = None,
        test_size: float = 0.2,
        perform_grid_search: bool = True,
        alphas: list = None,
        cv_folds: int = 5
    ) -> InstitutionalMatchModel:
        """
        Pipeline completo de entrenamiento

        Args:
            dataset_path: Ruta del dataset CSV
            output_model_path: Ruta donde guardar modelo
            visualizations_dir: Directorio para graficas
            test_size: Proporcion del test set
            perform_grid_search: Si True, busca mejor alpha
            alphas: Lista de alphas para grid search
            cv_folds: Numero de folds para CV

        Returns:
            Modelo entrenado
        """
        print("="*70)
        print("PIPELINE DE ENTRENAMIENTO DEL MODELO")
        print("="*70)

        # 1. Cargar dataset
        X, y, feature_names = self.load_dataset(dataset_path)

        # 2. Split train/test
        X_train, X_test, y_train, y_test = self.train_test_split_data(X, y, test_size)

        # 3. Grid Search (opcional)
        if perform_grid_search:
            grid_results = self.grid_search_alpha(X_train, y_train, alphas, cv_folds)
            best_alpha = grid_results['best_alpha']
        else:
            best_alpha = 1.0
            print(f"\nSaltando Grid Search, usando alpha={best_alpha}")

        # 4. Entrenar modelo final
        model = self.train_with_cross_validation(
            X_train, y_train,
            alpha=best_alpha,
            cv_folds=cv_folds,
            feature_names=feature_names
        )

        # 5. Evaluar en test
        test_metrics = self.evaluate_model(model, X_test, y_test)

        # 6. Visualizaciones
        if visualizations_dir:
            print(f"\nGenerando visualizaciones...")
            self.plot_predictions(
                model, X_test, y_test,
                os.path.join(visualizations_dir, 'predictions_vs_real.png')
            )
            self.plot_residuals(
                model, X_test, y_test,
                os.path.join(visualizations_dir, 'residuals_plot.png')
            )

        # 7. Guardar modelo
        model.save(output_model_path)

        # 8. Resumen final
        print(f"\n{model.summary()}")

        print(f"\n{'='*70}")
        print(f"ENTRENAMIENTO COMPLETADO")
        print(f"{'='*70}")

        self.best_model = model
        return model


def main():
    """Script principal de entrenamiento"""
    import os

    # Obtener directorio base
    current_dir = os.path.dirname(__file__)
    base_dir = os.path.join(current_dir, '..')

    # Configuracion
    DATASET_PATH = os.path.join(base_dir, 'data', 'training_data', 'synthetic_dataset.csv')
    MODEL_OUTPUT_PATH = os.path.join(base_dir, 'trained_models', 'ridge_v1.joblib')
    VISUALIZATIONS_DIR = os.path.join(base_dir, 'visualizations')

    # Crear trainer
    trainer = ModelTrainer(random_state=42)

    # Entrenar
    model = trainer.full_training_pipeline(
        dataset_path=DATASET_PATH,
        output_model_path=MODEL_OUTPUT_PATH,
        visualizations_dir=VISUALIZATIONS_DIR,
        test_size=0.2,
        perform_grid_search=True,
        alphas=[0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
        cv_folds=5
    )

    return model


if __name__ == "__main__":
    model = main()
