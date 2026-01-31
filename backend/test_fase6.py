"""
Script de prueba para Fase 6
Ejecutar: python test_fase6.py
"""

import sys
import os

# Agregar el directorio al path
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()


def test_imports():
    """Prueba que todas las importaciones funcionen"""
    print("=" * 60)
    print("1. VERIFICANDO IMPORTACIONES")
    print("=" * 60)

    try:
        from app.main import app
        print("   [OK] app.main")

        from app.api.schemas.ml_schemas import (
            InstitutionalWeights,
            InstitutionalProfileCreate,
            CVEvaluationRequest
        )
        print("   [OK] app.api.schemas.ml_schemas")

        from app.services.ml_integration_service import MLIntegrationService, get_ml_service
        print("   [OK] app.services.ml_integration_service")

        from app.api.routes import ml_predictions, institutional_profiles
        print("   [OK] app.api.routes")

        print("\n   Todas las importaciones exitosas!")
        return True

    except Exception as e:
        print(f"   [ERROR] {e}")
        return False


def test_ml_service():
    """Prueba el servicio ML"""
    print("\n" + "=" * 60)
    print("2. VERIFICANDO SERVICIO ML")
    print("=" * 60)

    try:
        from app.services.ml_integration_service import get_ml_service

        service = get_ml_service()
        print(f"   Servicio creado: {type(service).__name__}")
        print(f"   Modelo cargado: {service.is_ready}")

        if service.is_ready:
            info = service.get_model_info()
            print(f"   Tipo de modelo: {info.get('model_type')}")
            print(f"   Alpha: {info.get('alpha')}")

            metrics = info.get('training_metrics', {})
            if metrics:
                print(f"   R2 Score: {metrics.get('r2_score', 'N/A')}")

        return True

    except Exception as e:
        print(f"   [ERROR] {e}")
        return False


def test_supabase_connection():
    """Prueba la conexion a Supabase"""
    print("\n" + "=" * 60)
    print("3. VERIFICANDO CONEXION SUPABASE")
    print("=" * 60)

    try:
        from app.db.client import supabase

        if supabase is None:
            print("   [ERROR] Cliente Supabase no inicializado")
            return False

        print("   Cliente Supabase conectado")

        # Probar query a institutional_profiles
        response = supabase.table("institutional_profiles").select("count", count="exact").execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        print(f"   Perfiles institucionales: {count}")

        # Probar query a cv_evaluations
        response = supabase.table("cv_evaluations").select("count", count="exact").execute()
        count = response.count if hasattr(response, 'count') else len(response.data)
        print(f"   Evaluaciones de CV: {count}")

        return True

    except Exception as e:
        print(f"   [ERROR] {e}")
        return False


def test_create_sample_profile():
    """Crea un perfil de prueba"""
    print("\n" + "=" * 60)
    print("4. CREANDO PERFIL DE PRUEBA")
    print("=" * 60)

    try:
        from app.db.client import supabase
        from datetime import datetime

        # Verificar si ya existe
        existing = supabase.table("institutional_profiles") \
            .select("id") \
            .eq("institution_name", "TechBolivia Test") \
            .execute()

        if existing.data:
            print("   Perfil de prueba ya existe")
            profile_id = existing.data[0]['id']
        else:
            # Crear perfil de prueba
            now = datetime.utcnow().isoformat()
            data = {
                'institution_name': 'TechBolivia Test',
                'sector': 'Tecnologia',
                'description': 'Perfil de prueba para verificar integracion',
                'weights': {
                    'hard_skills': 0.35,
                    'soft_skills': 0.15,
                    'experience': 0.25,
                    'education': 0.15,
                    'languages': 0.10
                },
                'requirements': {
                    'min_experience_years': 1.0,
                    'required_skills': ['Python', 'SQL'],
                    'preferred_skills': ['Docker', 'AWS'],
                    'required_education_level': 'Licenciatura',
                    'required_languages': ['Ingles']
                },
                'thresholds': {
                    'apto': 0.70,
                    'considerado': 0.50
                },
                'is_active': True,
                'created_at': now,
                'updated_at': now
            }

            response = supabase.table("institutional_profiles").insert(data).execute()

            if response.data:
                profile_id = response.data[0]['id']
                print(f"   Perfil creado exitosamente!")
            else:
                print("   [ERROR] No se pudo crear el perfil")
                return False

        print(f"   ID: {profile_id}")
        return profile_id

    except Exception as e:
        print(f"   [ERROR] {e}")
        return False


def test_ml_prediction():
    """Prueba una prediccion ML con datos de ejemplo"""
    print("\n" + "=" * 60)
    print("5. PROBANDO PREDICCION ML")
    print("=" * 60)

    try:
        from app.services.ml_integration_service import get_ml_service

        service = get_ml_service()

        if not service.is_ready:
            print("   [SKIP] Modelo no cargado")
            return False

        # Cargar perfiles
        profiles = service.load_all_active_profiles()
        print(f"   Perfiles activos cargados: {len(profiles)}")

        if not profiles:
            print("   [SKIP] No hay perfiles para probar")
            return False

        # Datos de CV de ejemplo (simulando output de Gemini)
        gemini_output = {
            'hard_skills': ['Python', 'React', 'SQL', 'Docker', 'AWS'],
            'soft_skills': ['Liderazgo', 'Trabajo en equipo', 'Comunicacion'],
            'education': [
                {
                    'degree': 'Ingenieria de Sistemas',
                    'institution': 'Universidad Mayor de San Andres',
                    'year': '2020'
                }
            ],
            'experience': [
                {
                    'role': 'Senior Developer',
                    'company': 'Tech Corp',
                    'duration': '3 anios',
                    'description': 'Desarrollo de aplicaciones web'
                }
            ],
            'personal_info': {
                'languages': ['Espanol (Nativo)', 'Ingles (B2)'],
                'summary': 'Desarrollador con 3 anos de experiencia'
            }
        }

        # Evaluar contra el primer perfil
        profile = profiles[0]
        print(f"   Evaluando contra: {profile['institution_name']}")

        result = service.evaluate_cv(gemini_output, profile)

        print(f"\n   RESULTADO:")
        print(f"   Match Score: {result['match_score']:.3f}")
        print(f"   Clasificacion: {result['classification']}")
        print(f"\n   Scores por dimension:")
        for dim, score in result['cv_scores'].items():
            print(f"     {dim}: {score:.3f}")

        return True

    except Exception as e:
        print(f"   [ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False


def test_recommendations():
    """Prueba el sistema de recomendaciones"""
    print("\n" + "=" * 60)
    print("6. PROBANDO RECOMENDACIONES")
    print("=" * 60)

    try:
        from app.services.ml_integration_service import get_ml_service

        service = get_ml_service()

        if not service.is_ready:
            print("   [SKIP] Modelo no cargado")
            return False

        # CV de ejemplo
        gemini_output = {
            'hard_skills': ['Python', 'JavaScript', 'SQL'],
            'soft_skills': ['Comunicacion', 'Trabajo en equipo'],
            'education': [{'degree': 'Licenciatura en Informatica', 'institution': 'EMI', 'year': '2021'}],
            'experience': [{'role': 'Developer', 'company': 'Startup', 'duration': '2 anios'}],
            'personal_info': {'languages': ['Espanol (Nativo)', 'Ingles (B1)']}
        }

        recommendations = service.get_recommendations(gemini_output, top_n=5)

        print(f"   Recomendaciones generadas: {len(recommendations)}")

        for rec in recommendations[:3]:
            print(f"\n   #{rec['rank']} {rec['institution_name']}")
            print(f"      Score: {rec['match_score']:.3f} - {rec['classification']}")
            print(f"      Fortaleza: {rec['main_strength']}")

        return True

    except Exception as e:
        print(f"   [ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "=" * 60)
    print("PRUEBAS DE INTEGRACION - FASE 6")
    print("=" * 60)

    results = []

    # 1. Importaciones
    results.append(("Importaciones", test_imports()))

    # 2. Servicio ML
    results.append(("Servicio ML", test_ml_service()))

    # 3. Supabase
    results.append(("Supabase", test_supabase_connection()))

    # 4. Crear perfil
    profile_result = test_create_sample_profile()
    results.append(("Crear Perfil", profile_result is not False))

    # 5. Prediccion ML
    results.append(("Prediccion ML", test_ml_prediction()))

    # 6. Recomendaciones
    results.append(("Recomendaciones", test_recommendations()))

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)

    passed = 0
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "[OK]" if result else "[X]"
        print(f"   {symbol} {name}: {status}")
        if result:
            passed += 1

    print(f"\n   Total: {passed}/{len(results)} pruebas pasaron")

    if passed == len(results):
        print("\n   FASE 6 VERIFICADA EXITOSAMENTE!")
    else:
        print("\n   Algunas pruebas fallaron. Revisa los errores arriba.")

    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
