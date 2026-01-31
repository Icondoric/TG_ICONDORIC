"""
Script de Entrenamiento del Modelo Ridge
Entrena el modelo usando el dataset sintetico de Fase 3
"""

import os
import sys

# Agregar el directorio raiz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app.ml.models import ModelTrainer


def main():
    """Funcion principal de entrenamiento"""

    # Obtener directorio base
    current_dir = os.path.dirname(__file__)
    base_dir = os.path.join(current_dir, '..')

    # Configuracion
    DATASET_PATH = os.path.join(base_dir, 'data', 'training_data', 'synthetic_dataset.csv')
    MODEL_OUTPUT_PATH = os.path.join(base_dir, 'trained_models', 'ridge_v1.joblib')
    VISUALIZATIONS_DIR = os.path.join(base_dir, 'visualizations')

    # Verificar que existe el dataset
    if not os.path.exists(DATASET_PATH):
        print(f"ERROR: Dataset no encontrado en {DATASET_PATH}")
        print("Ejecuta primero el generador de dataset (Fase 3)")
        return None

    print("="*70)
    print("ENTRENAMIENTO DEL MODELO RIDGE - FASE 4")
    print("="*70)

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

    # Mostrar informacion adicional
    print("\n" + "="*70)
    print("COEFICIENTES DEL MODELO")
    print("="*70)

    coefficients = model.get_coefficients()
    for name, coef in sorted(coefficients.items(), key=lambda x: abs(x[1]), reverse=True):
        print(f"   {name:30s}: {coef:+.4f}")

    print("\n" + "="*70)
    print("IMPORTANCIA DE FEATURES")
    print("="*70)

    importance = model.get_feature_importance()
    for name, imp in importance.items():
        bar = '#' * int(imp * 50)
        print(f"   {name:30s}: {imp:.4f} {bar}")

    return model


if __name__ == "__main__":
    model = main()
