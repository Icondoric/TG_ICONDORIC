"""
Test de Fase 4 - Modelo Ridge
Verifica que el modelo entrenado funciona correctamente
"""

import os
import sys

# Agregar el directorio raiz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from app.ml.models import InstitutionalMatchModel, MatchPredictor


def test_model_loading():
    """Test 1: Cargar modelo entrenado"""
    print("\n" + "="*60)
    print("TEST 1: Cargar modelo entrenado")
    print("="*60)

    model_path = os.path.join(
        os.path.dirname(__file__), '..',
        'app', 'ml', 'trained_models', 'ridge_v1.joblib'
    )

    if not os.path.exists(model_path):
        print(f"ERROR: Modelo no encontrado en {model_path}")
        return False

    model = InstitutionalMatchModel.load(model_path)

    print(f"   Modelo cargado correctamente")
    print(f"   Alpha: {model.alpha}")
    print(f"   Is trained: {model.is_trained}")
    print(f"   Features: {len(model.feature_names)}")

    assert model.is_trained
    assert len(model.feature_names) == 18

    print("   [OK] Test 1 pasado")
    return True


def test_prediction_with_sample():
    """Test 2: Prediccion con ejemplo sintetico"""
    print("\n" + "="*60)
    print("TEST 2: Prediccion con ejemplo sintetico")
    print("="*60)

    predictor = MatchPredictor()

    # Feature vector de ejemplo (18 dimensiones)
    # CV Scores: hard=0.8, soft=0.7, exp=0.6, edu=0.92, lang=0.5
    # Weights: 0.35, 0.20, 0.25, 0.15, 0.05
    # Interactions: score * weight
    # Context: total_years=5, min_required=2, delta=3

    feature_vector = np.array([
        # CV Scores (5)
        0.8, 0.7, 0.6, 0.92, 0.5,
        # Weights (5)
        0.35, 0.20, 0.25, 0.15, 0.05,
        # Interactions (5)
        0.8*0.35, 0.7*0.20, 0.6*0.25, 0.92*0.15, 0.5*0.05,
        # Context (3)
        5.0, 2.0, 3.0
    ])

    result = predictor.model.predict_single(feature_vector)

    print(f"   Match Score: {result['match_score']:.4f}")
    print(f"   Clasificacion: {result['classification']}")
    print(f"\n   Top Fortalezas:")
    for feat, val in result['top_strengths']:
        print(f"      - {feat}: {val:+.4f}")

    assert 'match_score' in result
    assert 'classification' in result
    assert result['match_score'] >= 0 and result['match_score'] <= 1

    print("\n   [OK] Test 2 pasado")
    return True


def test_batch_prediction():
    """Test 3: Prediccion en batch"""
    print("\n" + "="*60)
    print("TEST 3: Prediccion en batch")
    print("="*60)

    predictor = MatchPredictor()

    # Generar 5 ejemplos aleatorios
    np.random.seed(42)
    feature_vectors = []

    for _ in range(5):
        cv_scores = np.random.beta(5, 2, 5)
        weights = np.random.dirichlet([2, 2, 2, 2, 2])
        interactions = cv_scores * weights
        context = [np.random.gamma(3, 1), np.random.uniform(0, 5), 0]
        context[2] = context[0] - context[1]

        fv = np.concatenate([cv_scores, weights, interactions, context])
        feature_vectors.append(fv)

    predictions = predictor.batch_predict(feature_vectors)

    print(f"   Predicciones generadas: {len(predictions)}")
    for i, pred in enumerate(predictions):
        print(f"   Ejemplo {i+1}: {pred['match_score']:.3f} -> {pred['classification']}")

    assert len(predictions) == 5

    print("\n   [OK] Test 3 pasado")
    return True


def test_model_info():
    """Test 4: Obtener informacion del modelo"""
    print("\n" + "="*60)
    print("TEST 4: Informacion del modelo")
    print("="*60)

    predictor = MatchPredictor()
    info = predictor.get_model_info()

    print(f"   Status: {info['status']}")
    print(f"   Tipo: {info['model_type']}")
    print(f"   Alpha: {info['alpha']}")
    print(f"   Normalizado: {info['normalize']}")
    print(f"   Features: {info['feature_count']}")
    print(f"   Intercepto: {info['intercept']:.4f}")
    print(f"\n   Metricas de entrenamiento:")
    for metric, value in info['training_metrics'].items():
        print(f"      {metric}: {value:.4f}")

    assert info['status'] == 'loaded'
    assert info['is_trained'] == True

    print("\n   [OK] Test 4 pasado")
    return True


def test_feature_importance():
    """Test 5: Importancia de features"""
    print("\n" + "="*60)
    print("TEST 5: Importancia de features")
    print("="*60)

    predictor = MatchPredictor()
    importance = predictor.model.get_feature_importance()

    print("   Top 5 features mas importantes:")
    for i, (name, imp) in enumerate(list(importance.items())[:5], 1):
        bar = '#' * int(imp * 50)
        print(f"   {i}. {name:30s}: {imp:.4f} {bar}")

    assert len(importance) == 18
    total_imp = sum(importance.values())
    assert abs(total_imp - 1.0) < 0.01  # Debe sumar ~1.0

    print("\n   [OK] Test 5 pasado")
    return True


def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*60)
    print("TESTS DE FASE 4 - MODELO RIDGE")
    print("="*60)

    tests = [
        test_model_loading,
        test_prediction_with_sample,
        test_batch_prediction,
        test_model_info,
        test_feature_importance,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   ERROR: {e}")
            failed += 1

    print("\n" + "="*60)
    print("RESUMEN DE TESTS")
    print("="*60)
    print(f"   Pasados: {passed}/{len(tests)}")
    print(f"   Fallados: {failed}/{len(tests)}")
    print("="*60)

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
