"""
Script de Generacion de Reporte de Evaluacion - Fase 5
Genera reporte completo de metricas y visualizaciones del modelo
"""

import os
import sys

# Agregar directorio raiz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score

from app.ml.models import InstitutionalMatchModel
from app.ml.evaluation.metrics import ModelEvaluator
from app.ml.evaluation.visualizations import ModelVisualizer


def main():
    """
    Funcion principal que genera el reporte completo de evaluacion
    """
    print("=" * 70)
    print("GENERACION DE REPORTE DE EVALUACION - FASE 5")
    print("=" * 70)

    # === CONFIGURACION ===
    current_dir = os.path.dirname(__file__)
    base_dir = os.path.join(current_dir, '..')

    MODEL_PATH = os.path.join(base_dir, 'trained_models', 'ridge_v1.joblib')
    DATASET_PATH = os.path.join(base_dir, 'data', 'training_data', 'synthetic_dataset.csv')
    OUTPUT_DIR = os.path.join(base_dir, 'evaluation_results')
    VISUALIZATIONS_DIR = os.path.join(OUTPUT_DIR, 'graficas')
    REPORT_PATH = os.path.join(OUTPUT_DIR, 'evaluation_report.md')

    # Crear directorios
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)

    # === 1. CARGAR MODELO ===
    print("\n[1/6] Cargando modelo entrenado...")

    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Modelo no encontrado en {MODEL_PATH}")
        print("Ejecuta primero el script de entrenamiento (Fase 4)")
        return None

    model = InstitutionalMatchModel.load(MODEL_PATH)
    print(f"   Modelo cargado: Ridge (alpha={model.alpha})")

    # === 2. CARGAR DATASET ===
    print("\n[2/6] Cargando dataset...")

    if not os.path.exists(DATASET_PATH):
        print(f"ERROR: Dataset no encontrado en {DATASET_PATH}")
        return None

    df = pd.read_csv(DATASET_PATH)
    feature_cols = [col for col in df.columns if col not in ['match_score', 'classification']]

    X = df[feature_cols].values
    y = df['match_score'].values

    print(f"   Dataset: {len(X)} ejemplos, {len(feature_cols)} features")

    # Split train/test (mismo que en entrenamiento)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   Train: {len(X_train)}, Test: {len(X_test)}")

    # === 3. CALCULAR METRICAS ===
    print("\n[3/6] Calculando metricas de evaluacion...")

    evaluator = ModelEvaluator()
    evaluation = evaluator.evaluate_model(model, X_test, y_test, feature_cols)

    # Calcular CV scores
    print("   Calculando Cross-Validation scores...")
    cv_scores = cross_val_score(
        model.model, X_train, y_train,
        cv=5, scoring='r2', n_jobs=-1
    )
    print(f"   CV R2: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")

    # === 4. COMPARAR CON BASELINE ===
    print("\n[4/6] Comparando con baselines...")

    comparison = evaluator.compare_with_baseline(
        model, X_test, y_test, X_train, y_train
    )

    print(f"   Ridge R2:       {comparison['ridge_model']['r2_score']:.4f}")
    print(f"   Baseline Media: {comparison['baseline_mean']['r2_score']:.4f}")
    if 'baseline_linear_regression' in comparison:
        print(f"   Linear Reg:     {comparison['baseline_linear_regression']['r2_score']:.4f}")

    # === 5. GENERAR VISUALIZACIONES ===
    print("\n[5/6] Generando visualizaciones...")

    visualizer = ModelVisualizer()
    generated_files = visualizer.create_full_evaluation_report(
        model=model,
        X_test=X_test,
        y_test=y_test,
        feature_names=feature_cols,
        cv_scores=cv_scores.tolist(),
        X_full=X,
        y_full=y,
        output_dir=VISUALIZATIONS_DIR
    )

    # === 6. GENERAR REPORTE ===
    print("\n[6/6] Generando reporte de metricas...")

    # Agregar info adicional al evaluation
    evaluation['cv_scores'] = cv_scores.tolist()
    evaluation['cv_mean'] = cv_scores.mean()
    evaluation['cv_std'] = cv_scores.std()

    # Generar reporte en texto
    report_text = evaluator.generate_metrics_report(evaluation, save_path=REPORT_PATH)

    # Agregar seccion de comparacion al reporte
    comparison_text = generate_comparison_section(comparison)

    # Agregar seccion de visualizaciones
    viz_text = generate_visualizations_section(generated_files)

    # Reporte completo
    full_report = report_text + "\n" + comparison_text + "\n" + viz_text

    # Guardar reporte completo
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(full_report)

    # === RESUMEN FINAL ===
    print("\n" + "=" * 70)
    print("EVALUACION COMPLETADA EXITOSAMENTE")
    print("=" * 70)

    print(f"\nArchivos generados:")
    print(f"   Reporte:        {REPORT_PATH}")
    print(f"   Visualizaciones: {VISUALIZATIONS_DIR}/")

    for name, path in generated_files.items():
        print(f"      - {os.path.basename(path)}")

    # Resumen de metricas
    reg = evaluation['regression_metrics']
    clf = evaluation['classification_metrics']

    print(f"\nResumen de Metricas:")
    print(f"   R2 Score:  {reg['r2_score']:.4f}")
    print(f"   RMSE:      {reg['rmse']:.4f}")
    print(f"   MAE:       {reg['mae']:.4f}")
    print(f"   Accuracy:  {clf['accuracy']:.4f}")

    # Verificar objetivos
    print(f"\nVerificacion de Objetivos:")
    objectives = [
        ('R2 >= 0.75', reg['r2_score'] >= 0.75),
        ('RMSE <= 0.17', reg['rmse'] <= 0.17),
        ('MAE <= 0.12', reg['mae'] <= 0.12),
        ('Accuracy >= 0.80', clf['accuracy'] >= 0.80)
    ]

    all_passed = True
    for name, passed in objectives:
        status = "CUMPLE" if passed else "NO CUMPLE"
        symbol = "[OK]" if passed else "[X]"
        print(f"   {symbol} {name}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n   TODOS LOS OBJETIVOS CUMPLIDOS")
    else:
        print("\n   Algunos objetivos no cumplidos - revisar modelo")

    return evaluation


def generate_comparison_section(comparison: dict) -> str:
    """Genera seccion de comparacion con baselines"""
    lines = []
    lines.append("\n" + "=" * 60)
    lines.append("COMPARACION CON BASELINES")
    lines.append("=" * 60)
    lines.append("")

    lines.append("Modelo          | R2 Score | RMSE    | MAE")
    lines.append("-" * 50)

    ridge = comparison['ridge_model']
    lines.append(f"Ridge           | {ridge['r2_score']:.4f}   | {ridge['rmse']:.4f} | {ridge['mae']:.4f}")

    mean = comparison['baseline_mean']
    lines.append(f"Baseline Media  | {mean['r2_score']:.4f}   | {mean['rmse']:.4f} | {mean['mae']:.4f}")

    median = comparison['baseline_median']
    lines.append(f"Baseline Mediana| {median['r2_score']:.4f}   | {median['rmse']:.4f} | {median['mae']:.4f}")

    if 'baseline_linear_regression' in comparison:
        lr = comparison['baseline_linear_regression']
        lines.append(f"Linear Reg      | {lr['r2_score']:.4f}   | {lr['rmse']:.4f} | {lr['mae']:.4f}")

    lines.append("")

    # Mejora relativa
    imp = comparison['improvement']
    lines.append("Mejora vs Baselines:")
    lines.append(f"  vs Media:  R2 +{imp['vs_mean']['r2_improvement']:.4f}, RMSE -{imp['vs_mean']['rmse_reduction']:.4f}")
    lines.append(f"  vs Mediana: R2 +{imp['vs_median']['r2_improvement']:.4f}, RMSE -{imp['vs_median']['rmse_reduction']:.4f}")

    return "\n".join(lines)


def generate_visualizations_section(files: dict) -> str:
    """Genera seccion listando visualizaciones"""
    lines = []
    lines.append("\n" + "=" * 60)
    lines.append("VISUALIZACIONES GENERADAS")
    lines.append("=" * 60)
    lines.append("")

    for name, path in files.items():
        filename = os.path.basename(path)
        description = {
            'feature_importance': 'Importancia de features (coeficientes)',
            'predictions_vs_actual': 'Predicciones vs valores reales',
            'residuals_distribution': 'Distribucion de residuos',
            'confusion_matrix': 'Matriz de confusion 3x3',
            'score_distribution_by_class': 'Boxplots por clase',
            'cv_scores_distribution': 'Scores de Cross-Validation',
            'learning_curve': 'Curva de aprendizaje',
            'coefficients_heatmap': 'Mapa de calor de coeficientes'
        }.get(name, name)

        lines.append(f"  - {filename}: {description}")

    return "\n".join(lines)


if __name__ == "__main__":
    evaluation = main()
