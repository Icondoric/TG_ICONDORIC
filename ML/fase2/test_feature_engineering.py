"""
Script de prueba para Feature Engineering
Valida que todos los scorers funcionen correctamente
"""

import json
import sys
import os

# Simular imports (ajustar según tu estructura real)
# from app.ml.feature_engineering import extract_features

# === CV DE EJEMPLO (Output simulado de Gemini) ===

gemini_output_ejemplo = {
    "personal_info": {
        "summary": "Ingeniero de Sistemas con 3 años de experiencia en desarrollo web",
        "languages": ["Español (Nativo)", "Inglés (B2)", "Francés (A2)"]
    },
    "hard_skills": [
        "Python", "JavaScript", "React", "SQL", "Git",
        "FastAPI", "PostgreSQL", "Docker", "HTML", "CSS"
    ],
    "soft_skills": [
        "Liderazgo", "Trabajo en equipo", "Comunicación",
        "Resolución de problemas", "Adaptabilidad"
    ],
    "education": [
        {
            "degree": "Ingeniería de Sistemas",
            "institution": "Escuela Militar de Ingeniería",
            "year": "2021"
        }
    ],
    "experience": [
        {
            "role": "Full Stack Developer",
            "company": "TechBolivia",
            "duration": "2 años",
            "description": "Desarrollo de aplicaciones web con React y FastAPI"
        },
        {
            "role": "Junior Developer",
            "company": "StartupX",
            "duration": "1 año",
            "description": "Mantenimiento de APIs REST"
        }
    ]
}

# === PERFIL INSTITUCIONAL DE EJEMPLO ===

institutional_config_ejemplo = {
    "institution_name": "TechBolivia Startup",
    "weights": {
        "hard_skills": 0.45,
        "soft_skills": 0.15,
        "experience": 0.20,
        "education": 0.10,
        "languages": 0.10
    },
    "requirements": {
        "min_experience_years": 1.5,
        "required_skills": ["Python", "JavaScript", "SQL"],
        "preferred_skills": ["React", "Docker", "AWS"],
        "required_soft_skills": ["Trabajo en equipo", "Comunicación"],
        "required_education_level": "Licenciatura",
        "required_languages": ["Inglés"]
    }
}

# === FUNCIONES DE PRUEBA ===

def test_hard_skills_scorer():
    """Prueba del scorer de hard skills"""
    print("\n=== TEST: Hard Skills Scorer ===")
    
    from hard_skills_scorer import calculate_hard_skills_score
    
    result = calculate_hard_skills_score(
        cv_skills=gemini_output_ejemplo['hard_skills'],
        required_skills=institutional_config_ejemplo['requirements']['required_skills'],
        preferred_skills=institutional_config_ejemplo['requirements']['preferred_skills']
    )
    
    print(f"Score: {result['score']}")
    print(f"Required match: {result['required_match_ratio']}")
    print(f"Matched: {result['matched_required']}")
    print(f"Missing: {result['missing_required']}")
    
    assert 0 <= result['score'] <= 1, "Score debe estar entre 0 y 1"
    assert len(result['matched_required']) > 0, "Debe haber al menos un match"
    print("✅ PASS")


def test_soft_skills_scorer():
    """Prueba del scorer de soft skills"""
    print("\n=== TEST: Soft Skills Scorer ===")
    
    from soft_skills_scorer import calculate_soft_skills_score
    
    result = calculate_soft_skills_score(
        cv_soft_skills=gemini_output_ejemplo['soft_skills'],
        required_soft_skills=institutional_config_ejemplo['requirements']['required_soft_skills']
    )
    
    print(f"Score: {result['score']}")
    print(f"Exact match ratio: {result['exact_match_ratio']}")
    print(f"Matched: {result['matched_exact']}")
    
    assert 0 <= result['score'] <= 1, "Score debe estar entre 0 y 1"
    print("✅ PASS")


def test_education_scorer():
    """Prueba del scorer de educación"""
    print("\n=== TEST: Education Scorer ===")
    
    from education_scorer import calculate_education_score
    
    result = calculate_education_score(
        cv_education=gemini_output_ejemplo['education'],
        required_education_level=institutional_config_ejemplo['requirements']['required_education_level']
    )
    
    print(f"Score: {result['score']}")
    print(f"CV level: {result['cv_level']}")
    print(f"Meets requirement: {result['meets_requirement']}")
    
    assert 0 <= result['score'] <= 1, "Score debe estar entre 0 y 1"
    print("✅ PASS")


def test_experience_scorer():
    """Prueba del scorer de experiencia"""
    print("\n=== TEST: Experience Scorer ===")
    
    from experience_scorer import calculate_experience_score_from_cv
    
    result = calculate_experience_score_from_cv(
        cv_experience=gemini_output_ejemplo['experience'],
        min_required_years=institutional_config_ejemplo['requirements']['min_experience_years']
    )
    
    print(f"Score: {result['score']}")
    print(f"Total years: {result['total_years']}")
    print(f"Classification: {result['classification']}")
    print(f"Meets minimum: {result['meets_minimum']}")
    
    assert 0 <= result['score'] <= 1, "Score debe estar entre 0 y 1"
    assert result['total_years'] > 0, "Debe tener experiencia"
    print("✅ PASS")


def test_languages_scorer():
    """Prueba del scorer de idiomas"""
    print("\n=== TEST: Languages Scorer ===")
    
    from languages_scorer import calculate_languages_score_from_cv
    
    result = calculate_languages_score_from_cv(
        cv_languages=gemini_output_ejemplo['personal_info']['languages'],
        required_languages=institutional_config_ejemplo['requirements']['required_languages']
    )
    
    print(f"Score: {result['score']}")
    print(f"Matched: {result['matched']}")
    print(f"Missing: {result['missing']}")
    
    assert 0 <= result['score'] <= 1, "Score debe estar entre 0 y 1"
    print("✅ PASS")


def test_feature_extractor():
    """Prueba del orquestador completo"""
    print("\n=== TEST: Feature Extractor (COMPLETO) ===")
    
    from feature_extractor import extract_features, get_feature_names
    
    result = extract_features(
        gemini_output=gemini_output_ejemplo,
        institutional_config=institutional_config_ejemplo
    )
    
    print(f"\n📊 CV Scores:")
    for key, value in result['cv_scores'].items():
        print(f"  {key}: {value}")
    
    print(f"\n⚙️ Institutional Params:")
    for key, value in result['institutional_params'].items():
        print(f"  {key}: {value}")
    
    print(f"\n🔢 Feature Vector ({len(result['feature_vector'])} features):")
    feature_names = get_feature_names()
    for i, (name, value) in enumerate(zip(feature_names, result['feature_vector'])):
        print(f"  [{i}] {name}: {value:.3f}")
    
    # Validaciones
    assert len(result['feature_vector']) == 18, "Debe haber 18 features"
    assert result['feature_vector_array'].shape == (1, 18), "Shape debe ser (1, 18)"
    assert all(isinstance(x, (int, float)) for x in result['feature_vector']), "Todos deben ser numéricos"
    
    print("\n✅ PASS - Feature Extraction completa exitosa")
    
    return result


def save_feature_vector_example(features_result):
    """Guarda un ejemplo de feature vector para documentación"""
    
    output = {
        "cv_scores": features_result['cv_scores'],
        "institutional_params": features_result['institutional_params'],
        "feature_vector": features_result['feature_vector'],
        "feature_names": get_feature_names(),
        "metadata_summary": {
            "total_features": features_result['metadata']['total_features'],
            "hard_skills_matched": features_result['metadata']['hard_skills_details']['matched_required'],
            "experience_classification": features_result['metadata']['experience_details']['classification']
        }
    }
    
    with open('feature_vector_example.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("\n💾 Feature vector guardado en: feature_vector_example.json")


if __name__ == "__main__":
    print("="*60)
    print("PRUEBAS DE FEATURE ENGINEERING")
    print("="*60)
    
    try:
        # Ejecutar todas las pruebas
        test_hard_skills_scorer()
        test_soft_skills_scorer()
        test_education_scorer()
        test_experience_scorer()
        test_languages_scorer()
        
        # Prueba completa
        features = test_feature_extractor()
        
        # Guardar ejemplo
        save_feature_vector_example(features)
        
        print("\n" + "="*60)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
