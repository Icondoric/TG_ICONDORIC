"""
Model Evaluator - Fase 5
Calculo de metricas de evaluacion del modelo
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor


class ModelEvaluator:
    """
    Evaluador de modelos de Machine Learning

    Calcula metricas de regresion y clasificacion para evaluar
    el rendimiento del modelo de matching institucional.
    """

    # Umbrales de clasificacion
    THRESHOLD_APTO = 0.70
    THRESHOLD_CONSIDERADO = 0.50

    # Nombres de clases
    CLASS_NAMES = ['NO_APTO', 'CONSIDERADO', 'APTO']

    def __init__(self):
        """Inicializa el evaluador"""
        self.last_evaluation = None

    def _score_to_class(self, score: float) -> str:
        """
        Convierte un score a clasificacion

        Args:
            score: Score de matching [0-1]

        Returns:
            Clasificacion: APTO, CONSIDERADO o NO_APTO
        """
        if score >= self.THRESHOLD_APTO:
            return 'APTO'
        elif score >= self.THRESHOLD_CONSIDERADO:
            return 'CONSIDERADO'
        else:
            return 'NO_APTO'

    def _scores_to_classes(self, scores: np.ndarray) -> np.ndarray:
        """
        Convierte array de scores a clasificaciones

        Args:
            scores: Array de scores

        Returns:
            Array de clasificaciones
        """
        return np.array([self._score_to_class(s) for s in scores])

    def calculate_regression_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Dict[str, float]:
        """
        Calcula metricas de regresion

        Args:
            y_true: Valores reales
            y_pred: Valores predichos

        Returns:
            Dict con metricas de regresion
        """
        # Validar dimensiones
        if len(y_true) != len(y_pred):
            raise ValueError(f"Dimensiones no coinciden: y_true={len(y_true)}, y_pred={len(y_pred)}")

        # Convertir a arrays numpy
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        # Calcular metricas
        r2 = r2_score(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)

        # MAPE (evitar division por cero)
        mask = y_true != 0
        if mask.sum() > 0:
            mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
        else:
            mape = None

        # Residuos
        residuals = y_true - y_pred
        residuals_mean = np.mean(residuals)
        residuals_std = np.std(residuals)

        return {
            'r2_score': r2,
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'mape': mape,
            'residuals_mean': residuals_mean,
            'residuals_std': residuals_std,
            'n_samples': len(y_true)
        }

    def calculate_classification_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Dict:
        """
        Calcula metricas de clasificacion

        Args:
            y_true: Valores reales (scores)
            y_pred: Valores predichos (scores)

        Returns:
            Dict con metricas de clasificacion y confusion matrix
        """
        # Convertir scores a clases
        y_true_class = self._scores_to_classes(y_true)
        y_pred_class = self._scores_to_classes(y_pred)

        # Accuracy general
        accuracy = accuracy_score(y_true_class, y_pred_class)

        # Metricas por clase
        precision = precision_score(
            y_true_class, y_pred_class,
            labels=self.CLASS_NAMES,
            average=None,
            zero_division=0
        )
        recall = recall_score(
            y_true_class, y_pred_class,
            labels=self.CLASS_NAMES,
            average=None,
            zero_division=0
        )
        f1 = f1_score(
            y_true_class, y_pred_class,
            labels=self.CLASS_NAMES,
            average=None,
            zero_division=0
        )

        # Metricas weighted y macro
        precision_weighted = precision_score(
            y_true_class, y_pred_class,
            labels=self.CLASS_NAMES,
            average='weighted',
            zero_division=0
        )
        recall_weighted = recall_score(
            y_true_class, y_pred_class,
            labels=self.CLASS_NAMES,
            average='weighted',
            zero_division=0
        )
        f1_weighted = f1_score(
            y_true_class, y_pred_class,
            labels=self.CLASS_NAMES,
            average='weighted',
            zero_division=0
        )

        # Matriz de confusion
        cm = confusion_matrix(
            y_true_class, y_pred_class,
            labels=self.CLASS_NAMES
        )

        # Distribucion de clases
        unique_true, counts_true = np.unique(y_true_class, return_counts=True)
        unique_pred, counts_pred = np.unique(y_pred_class, return_counts=True)

        class_distribution_true = dict(zip(unique_true, counts_true.astype(int)))
        class_distribution_pred = dict(zip(unique_pred, counts_pred.astype(int)))

        return {
            'accuracy': accuracy,
            'precision_by_class': dict(zip(self.CLASS_NAMES, precision)),
            'recall_by_class': dict(zip(self.CLASS_NAMES, recall)),
            'f1_by_class': dict(zip(self.CLASS_NAMES, f1)),
            'precision_weighted': precision_weighted,
            'recall_weighted': recall_weighted,
            'f1_weighted': f1_weighted,
            'confusion_matrix': cm,
            'class_names': self.CLASS_NAMES,
            'class_distribution_true': class_distribution_true,
            'class_distribution_pred': class_distribution_pred,
            'n_samples': len(y_true)
        }

    def evaluate_model(
        self,
        model,
        X_test: np.ndarray,
        y_test: np.ndarray,
        feature_names: List[str] = None
    ) -> Dict:
        """
        Evaluacion completa del modelo

        Args:
            model: Modelo entrenado (con metodo predict)
            X_test: Features de test
            y_test: Target de test
            feature_names: Nombres de features (opcional)

        Returns:
            Dict completo con todas las metricas
        """
        # Verificar que el modelo este entrenado
        if not hasattr(model, 'is_trained') or not model.is_trained:
            raise ValueError("El modelo no ha sido entrenado")

        # Obtener predicciones
        y_pred = model.predict(X_test)

        # Calcular metricas de regresion
        regression_metrics = self.calculate_regression_metrics(y_test, y_pred)

        # Calcular metricas de clasificacion
        classification_metrics = self.calculate_classification_metrics(y_test, y_pred)

        # Feature importance del modelo
        feature_importance = {}
        if hasattr(model, 'get_feature_importance'):
            feature_importance = model.get_feature_importance()
        elif hasattr(model, 'get_coefficients'):
            coeffs = model.get_coefficients()
            # Normalizar coeficientes
            total = sum(abs(v) for v in coeffs.values())
            if total > 0:
                feature_importance = {k: abs(v)/total for k, v in coeffs.items()}

        # Coeficientes del modelo
        coefficients = {}
        if hasattr(model, 'get_coefficients'):
            coefficients = model.get_coefficients()

        # Intercepto
        intercept = None
        if hasattr(model, 'get_intercept'):
            intercept = model.get_intercept()

        # Informacion del modelo
        model_info = {
            'type': 'Ridge Regression',
            'alpha': getattr(model, 'alpha', None),
            'normalize': getattr(model, 'normalize', None),
            'intercept': intercept
        }

        # Compilar resultado
        evaluation = {
            'model_info': model_info,
            'regression_metrics': regression_metrics,
            'classification_metrics': classification_metrics,
            'feature_importance': feature_importance,
            'coefficients': coefficients,
            'feature_names': feature_names,
            'predictions': {
                'y_true': y_test,
                'y_pred': y_pred
            }
        }

        # Guardar ultima evaluacion
        self.last_evaluation = evaluation

        return evaluation

    def compare_with_baseline(
        self,
        model,
        X_test: np.ndarray,
        y_test: np.ndarray,
        X_train: np.ndarray = None,
        y_train: np.ndarray = None
    ) -> Dict:
        """
        Compara el modelo con baselines simples

        Args:
            model: Modelo a evaluar
            X_test: Features de test
            y_test: Target de test
            X_train: Features de train (para entrenar baseline)
            y_train: Target de train (para entrenar baseline)

        Returns:
            Dict con comparacion de metricas
        """
        # Predicciones del modelo
        y_pred_model = model.predict(X_test)

        # Baseline 1: Media
        baseline_mean = DummyRegressor(strategy='mean')
        if X_train is not None and y_train is not None:
            baseline_mean.fit(X_train, y_train)
        else:
            # Usar media del test set
            baseline_mean.fit(X_test, y_test)
        y_pred_mean = baseline_mean.predict(X_test)

        # Baseline 2: Mediana
        baseline_median = DummyRegressor(strategy='median')
        if X_train is not None and y_train is not None:
            baseline_median.fit(X_train, y_train)
        else:
            baseline_median.fit(X_test, y_test)
        y_pred_median = baseline_median.predict(X_test)

        # Baseline 3: Regresion lineal simple (sin regularizacion)
        baseline_lr = LinearRegression()
        if X_train is not None and y_train is not None:
            baseline_lr.fit(X_train, y_train)
            y_pred_lr = baseline_lr.predict(X_test)
        else:
            y_pred_lr = None

        # Calcular metricas para cada modelo
        metrics_model = self.calculate_regression_metrics(y_test, y_pred_model)
        metrics_mean = self.calculate_regression_metrics(y_test, y_pred_mean)
        metrics_median = self.calculate_regression_metrics(y_test, y_pred_median)

        comparison = {
            'ridge_model': metrics_model,
            'baseline_mean': metrics_mean,
            'baseline_median': metrics_median,
        }

        if y_pred_lr is not None:
            metrics_lr = self.calculate_regression_metrics(y_test, y_pred_lr)
            comparison['baseline_linear_regression'] = metrics_lr

        # Calcular mejora relativa
        improvement = {
            'vs_mean': {
                'r2_improvement': metrics_model['r2_score'] - metrics_mean['r2_score'],
                'rmse_reduction': metrics_mean['rmse'] - metrics_model['rmse'],
                'mae_reduction': metrics_mean['mae'] - metrics_model['mae']
            },
            'vs_median': {
                'r2_improvement': metrics_model['r2_score'] - metrics_median['r2_score'],
                'rmse_reduction': metrics_median['rmse'] - metrics_model['rmse'],
                'mae_reduction': metrics_median['mae'] - metrics_model['mae']
            }
        }

        if y_pred_lr is not None:
            improvement['vs_linear_regression'] = {
                'r2_improvement': metrics_model['r2_score'] - metrics_lr['r2_score'],
                'rmse_reduction': metrics_lr['rmse'] - metrics_model['rmse'],
                'mae_reduction': metrics_lr['mae'] - metrics_model['mae']
            }

        comparison['improvement'] = improvement

        return comparison

    def generate_metrics_report(
        self,
        evaluation_results: Dict,
        save_path: str = None
    ) -> str:
        """
        Genera reporte de metricas en formato texto/markdown

        Args:
            evaluation_results: Resultado de evaluate_model()
            save_path: Ruta para guardar el reporte (opcional)

        Returns:
            String con el reporte formateado
        """
        reg = evaluation_results['regression_metrics']
        clf = evaluation_results['classification_metrics']
        model_info = evaluation_results['model_info']
        feature_importance = evaluation_results.get('feature_importance', {})

        report = []
        report.append("=" * 60)
        report.append("REPORTE DE EVALUACION DEL MODELO")
        report.append("=" * 60)
        report.append("")

        # Info del modelo
        report.append("INFORMACION DEL MODELO")
        report.append("-" * 40)
        report.append(f"Tipo: {model_info['type']}")
        report.append(f"Alpha (regularizacion): {model_info['alpha']}")
        report.append(f"Normalizacion: {'Si' if model_info['normalize'] else 'No'}")
        report.append(f"Intercepto: {model_info['intercept']:.4f}" if model_info['intercept'] else "")
        report.append(f"Ejemplos evaluados: {reg['n_samples']}")
        report.append("")

        # Metricas de regresion
        report.append("METRICAS DE REGRESION")
        report.append("-" * 40)
        report.append(f"R2 Score:  {reg['r2_score']:.4f}")
        report.append(f"MSE:       {reg['mse']:.4f}")
        report.append(f"RMSE:      {reg['rmse']:.4f}")
        report.append(f"MAE:       {reg['mae']:.4f}")
        if reg['mape'] is not None:
            report.append(f"MAPE:      {reg['mape']:.2f}%")
        report.append("")
        report.append(f"Media de residuos:     {reg['residuals_mean']:.6f}")
        report.append(f"Std de residuos:       {reg['residuals_std']:.4f}")
        report.append("")

        # Interpretacion de R2
        r2 = reg['r2_score']
        if r2 >= 0.80:
            interpretation = "Excelente - El modelo explica muy bien la varianza"
        elif r2 >= 0.70:
            interpretation = "Bueno - El modelo tiene buen poder predictivo"
        elif r2 >= 0.60:
            interpretation = "Aceptable - El modelo captura patrones principales"
        else:
            interpretation = "Insuficiente - Considerar mejorar el modelo"
        report.append(f"Interpretacion R2: {interpretation}")
        report.append("")

        # Metricas de clasificacion
        report.append("METRICAS DE CLASIFICACION")
        report.append("-" * 40)
        report.append(f"Accuracy: {clf['accuracy']:.4f} ({clf['accuracy']*100:.1f}%)")
        report.append("")

        report.append("Precision por clase:")
        for cls, val in clf['precision_by_class'].items():
            report.append(f"  {cls:15s}: {val:.4f}")
        report.append("")

        report.append("Recall por clase:")
        for cls, val in clf['recall_by_class'].items():
            report.append(f"  {cls:15s}: {val:.4f}")
        report.append("")

        report.append("F1-Score por clase:")
        for cls, val in clf['f1_by_class'].items():
            report.append(f"  {cls:15s}: {val:.4f}")
        report.append("")

        report.append(f"F1-Score Weighted: {clf['f1_weighted']:.4f}")
        report.append("")

        # Distribucion de clases
        report.append("Distribucion de clases (real vs predicho):")
        for cls in clf['class_names']:
            true_count = clf['class_distribution_true'].get(cls, 0)
            pred_count = clf['class_distribution_pred'].get(cls, 0)
            report.append(f"  {cls:15s}: {true_count:5d} real vs {pred_count:5d} predicho")
        report.append("")

        # Matriz de confusion
        report.append("Matriz de Confusion:")
        report.append("                  Predicho")
        report.append(f"                  {'  '.join([c[:4] for c in clf['class_names']])}")
        cm = clf['confusion_matrix']
        for i, cls in enumerate(clf['class_names']):
            row = "  ".join([f"{cm[i,j]:4d}" for j in range(len(clf['class_names']))])
            report.append(f"  Real {cls[:4]:6s}   {row}")
        report.append("")

        # Feature importance
        if feature_importance:
            report.append("IMPORTANCIA DE FEATURES (Top 10)")
            report.append("-" * 40)
            sorted_features = sorted(
                feature_importance.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
            for i, (name, imp) in enumerate(sorted_features, 1):
                bar = '#' * int(imp * 40)
                report.append(f"{i:2d}. {name:30s}: {imp:.4f} {bar}")
            report.append("")

        # Verificacion de objetivos
        report.append("VERIFICACION DE OBJETIVOS")
        report.append("-" * 40)

        objectives = [
            ('R2 >= 0.75', reg['r2_score'] >= 0.75, reg['r2_score']),
            ('RMSE <= 0.17', reg['rmse'] <= 0.17, reg['rmse']),
            ('MAE <= 0.12', reg['mae'] <= 0.12, reg['mae']),
            ('Accuracy >= 0.80', clf['accuracy'] >= 0.80, clf['accuracy'])
        ]

        for name, passed, value in objectives:
            status = "CUMPLE" if passed else "NO CUMPLE"
            report.append(f"  {name:20s}: {status:10s} (valor: {value:.4f})")
        report.append("")

        # Resumen
        all_passed = all(obj[1] for obj in objectives)
        report.append("=" * 60)
        if all_passed:
            report.append("RESULTADO: TODOS LOS OBJETIVOS CUMPLIDOS")
        else:
            passed_count = sum(1 for obj in objectives if obj[1])
            report.append(f"RESULTADO: {passed_count}/4 OBJETIVOS CUMPLIDOS")
        report.append("=" * 60)

        # Unir reporte
        report_text = "\n".join(report)

        # Guardar si se especifica ruta
        if save_path:
            import os
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"Reporte guardado en: {save_path}")

        return report_text


def evaluate_trained_model(model_path: str, dataset_path: str) -> Dict:
    """
    Funcion de conveniencia para evaluar un modelo guardado

    Args:
        model_path: Ruta al modelo .joblib
        dataset_path: Ruta al dataset CSV

    Returns:
        Dict con resultados de evaluacion
    """
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from app.ml.models import InstitutionalMatchModel

    # Cargar modelo
    model = InstitutionalMatchModel.load(model_path)

    # Cargar dataset
    df = pd.read_csv(dataset_path)
    feature_cols = [col for col in df.columns if col not in ['match_score', 'classification']]
    X = df[feature_cols].values
    y = df['match_score'].values

    # Split para obtener test set
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Evaluar
    evaluator = ModelEvaluator()
    results = evaluator.evaluate_model(model, X_test, y_test, feature_cols)

    return results
