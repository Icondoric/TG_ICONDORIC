# FASE 1 - IMPLEMENTACION COMPLETADA

**Fecha de implementacion:** 30 de enero de 2025
**Estado:** COMPLETADO

---

## RESUMEN EJECUTIVO

La Fase 1 establece las **definiciones base** del sistema de scoring para evaluacion de perfiles de candidatos. Se implementaron tres modulos principales que calculan scores normalizados [0-1] para educacion, idiomas y experiencia laboral, junto con un sistema de perfiles institucionales que permite personalizar los criterios de evaluacion segun el tipo de organizacion.

---

## ESTRUCTURA DE ARCHIVOS IMPLEMENTADOS

```
backend/app/
├── scoring/                              # MODULO DE SCORING
│   ├── __init__.py                       # Exporta todas las funciones
│   ├── education_levels.py               # Escalas de educacion
│   ├── language_levels.py                # Escalas de idiomas (CEFR)
│   └── experience_calculator.py          # Calculadora logaritmica
│
└── data/                                 # MODULO DE DATOS
    ├── __init__.py                       # Exporta funciones de carga
    ├── profile_loader.py                 # Utilidades para perfiles
    └── profiles/                         # Perfiles institucionales JSON
        ├── profile_agetic.json
        ├── profile_banco_fie.json
        ├── profile_drogueria_inti.json
        ├── profile_empacar.json
        └── profile_mopsv.json
```

---

## MODULO DE SCORING

### 1. education_levels.py
**Ruta:** `backend/app/scoring/education_levels.py`

Define la escala de niveles educativos basada en el sistema educativo boliviano:

```python
EDUCATION_LEVELS = {
    "Tecnico Medio": 0.25,
    "Tecnico Superior": 0.45,
    "Licenciatura": 0.75,
    "Ingenieria": 0.75,
    "Diplomado": 0.80,
    "Especialidad": 0.85,
    "Maestria": 0.92,
    "Doctorado": 1.00
}
```

**Funciones exportadas:**
- `get_education_score(degree_name: str) -> float`: Retorna score [0-1] con busqueda inteligente (fuzzy matching)
- `get_education_level_name(score: float) -> str`: Retorna nombre del nivel dado un score

**Ejemplo de uso:**
```python
from app.scoring import get_education_score

get_education_score("Ingenieria de Sistemas")  # -> 0.75
get_education_score("Maestria en Administracion")  # -> 0.92
get_education_score("PhD en Computacion")  # -> 1.00
```

---

### 2. language_levels.py
**Ruta:** `backend/app/scoring/language_levels.py`

Define la escala de niveles de idiomas basada en el Marco Comun Europeo de Referencia (CEFR):

```python
LANGUAGE_LEVELS = {
    "Basico": 0.30,
    "A1": 0.35, "A2": 0.45,
    "Intermedio": 0.55,
    "B1": 0.60, "B2": 0.75,
    "Avanzado": 0.85,
    "C1": 0.90, "C2": 0.95,
    "Nativo": 1.00, "Materno": 1.00,
    "Fluido": 0.80
}
```

**Funciones exportadas:**
- `get_language_score(language_description: str) -> float`: Extrae score de una descripcion
- `parse_language_entry(language_str: str) -> dict`: Parsea entrada completa (idioma, nivel, score)
- `calculate_languages_score(cv_languages: list, required_languages: list) -> dict`: Compara CV con requisitos

**Ejemplo de uso:**
```python
from app.scoring import calculate_languages_score

result = calculate_languages_score(
    cv_languages=["Espanol (Nativo)", "Ingles (B2)", "Portugues (A2)"],
    required_languages=["Ingles", "Frances"]
)
# -> {'score': 0.375, 'matched': ['Ingles'], 'missing': ['Frances'], 'details': [...]}
```

---

### 3. experience_calculator.py
**Ruta:** `backend/app/scoring/experience_calculator.py`

Implementa una **funcion logaritmica** para calcular el score de experiencia, reflejando el principio economico de rendimientos decrecientes:

- Los primeros anios de experiencia aportan mayor valor marginal
- Despues de cierto punto (max_ideal=5 anios por defecto), la experiencia adicional no suma
- Se penaliza proporcionalmente si no se cumple el minimo requerido

**Funciones exportadas:**
- `calculate_experience_score(years: float, min_required: float, max_ideal: float) -> dict`: Calcula score con curva logaritmica
- `parse_experience_duration(duration_str: str) -> float`: Parsea duraciones textuales ("2 anios", "6 meses", "2021-2023")
- `calculate_total_experience(experience_list: list) -> float`: Suma experiencias de una lista

**Ejemplo de uso:**
```python
from app.scoring import calculate_experience_score, parse_experience_duration

# Candidato con 3 anios, requisito minimo 1 anio
result = calculate_experience_score(3.0, min_required=1.0)
# -> {'score': 0.789, 'meets_minimum': True, 'classification': 'Experiencia muy buena', ...}

# Candidato que no cumple minimo
result = calculate_experience_score(0.5, min_required=2.0)
# -> {'score': 0.125, 'meets_minimum': False, 'classification': 'No cumple minimo requerido', ...}

# Parsear duracion textual
parse_experience_duration("2021 - presente")  # -> 4.0 (si estamos en 2025)
parse_experience_duration("18 meses")  # -> 1.5
```

---

## MODULO DE DATOS

### 4. profile_loader.py
**Ruta:** `backend/app/data/profile_loader.py`

Proporciona utilidades para cargar y validar perfiles institucionales:

**Funciones exportadas:**
- `get_available_profiles() -> List[str]`: Lista IDs de perfiles disponibles
- `load_profile(profile_id: str) -> Optional[Dict]`: Carga un perfil por ID
- `load_all_profiles() -> Dict[str, Dict]`: Carga todos los perfiles
- `validate_profile(profile: Dict) -> Dict`: Valida estructura de un perfil

**Ejemplo de uso:**
```python
from app.data import load_profile, get_available_profiles

# Ver perfiles disponibles
get_available_profiles()
# -> ['profile_agetic', 'profile_banco_fie', 'profile_drogueria_inti', 'profile_empacar', 'profile_mopsv']

# Cargar perfil especifico
profile = load_profile("profile_agetic")
print(profile["institution_name"])  # -> "AGETIC - Agencia de Gobierno Electronico y TICs"
print(profile["weights"])  # -> {'hard_skills': 0.40, 'soft_skills': 0.20, ...}
```

---

## PERFILES INSTITUCIONALES

Cada perfil define los criterios de evaluacion para una institucion especifica:

### Estructura de un perfil:
```json
{
  "id": "profile_agetic",
  "institution_name": "AGETIC - Agencia de Gobierno Electronico y TICs",
  "sector": "Gobierno - Tecnologia",
  "description": "...",

  "weights": {
    "hard_skills": 0.40,
    "soft_skills": 0.20,
    "experience": 0.20,
    "education": 0.15,
    "languages": 0.05
  },

  "requirements": {
    "min_experience_years": 1.5,
    "required_skills": ["Programacion", "Desarrollo de software", "Linux", "Git"],
    "preferred_skills": ["Python", "Java", "PostgreSQL", "DevOps"],
    "required_education_level": "Licenciatura",
    "required_languages": []
  },

  "thresholds": {
    "apto": 0.72,
    "considerado": 0.52
  }
}
```

### Perfiles implementados:

| Archivo | Institucion | Sector | Peso Principal |
|---------|-------------|--------|----------------|
| `profile_agetic.json` | AGETIC | Gobierno - Tecnologia | Hard Skills (40%) |
| `profile_banco_fie.json` | Banco FIE S.A. | Servicios Financieros | Hard Skills (30%) + Soft Skills (25%) |
| `profile_drogueria_inti.json` | Drogueria INTI | Farmaceutico - Salud | Soft Skills (30%) |
| `profile_empacar.json` | Empacar S.A. | Industria - Manufactura | Hard Skills (35%) + Experiencia (30%) |
| `profile_mopsv.json` | Min. Obras Publicas | Gobierno | Hard Skills (30%) + Experiencia (25%) |

**Validacion:** Todos los perfiles suman pesos = 1.00

---

## COMO USAR LOS MODULOS

### Importacion desde otros archivos del backend:

```python
# Importar funciones de scoring
from app.scoring import (
    get_education_score,
    calculate_experience_score,
    calculate_languages_score,
    parse_experience_duration
)

# Importar funciones de datos
from app.data import (
    load_profile,
    load_all_profiles,
    get_available_profiles
)
```

### Ejemplo de evaluacion completa de un candidato:

```python
from app.scoring import get_education_score, calculate_experience_score, calculate_languages_score
from app.data import load_profile

# Cargar perfil institucional
profile = load_profile("profile_agetic")

# Datos del candidato (extraidos del CV)
candidato = {
    "education": "Ingenieria de Sistemas",
    "experience_years": 2.5,
    "languages": ["Espanol (Nativo)", "Ingles (B1)"]
}

# Calcular scores individuales
edu_score = get_education_score(candidato["education"])
# -> 0.75

exp_result = calculate_experience_score(
    candidato["experience_years"],
    min_required=profile["requirements"]["min_experience_years"]
)
# -> {'score': 0.72, 'meets_minimum': True, ...}

lang_result = calculate_languages_score(
    candidato["languages"],
    profile["requirements"]["required_languages"]
)
# -> {'score': 1.0, 'matched': [], 'missing': []}  (no hay requisitos de idioma)
```

---

## DEPENDENCIAS

No se requieren dependencias adicionales. Los modulos usan solo librerias estandar de Python:
- `math` (para funcion logaritmica)
- `re` (para parsing de texto)
- `json` (para cargar perfiles)
- `os` (para manejo de rutas)
- `datetime` (para calcular "presente/actual")

---

## PRUEBAS REALIZADAS

Se verifico el funcionamiento correcto de todos los modulos:

```
=== Test Education ===
Ingenieria: 0.75
Maestria en Sistemas: 0.92
Licenciatura: 0.75

=== Test Experience ===
2 anios con min 1: score=0.685, meets_minimum=True
0.5 anios con min 2: score=0.125, meets_minimum=False

=== Test Languages ===
['Espanol (Nativo)', 'Ingles (B2)'] vs ['Ingles']: score=0.75

=== Test Profiles ===
profile_agetic: pesos suman 1.00
profile_banco_fie: pesos suman 1.00
profile_drogueria_inti: pesos suman 1.00
profile_empacar: pesos suman 1.00
profile_mopsv: pesos suman 1.00
```

---

## SIGUIENTE PASO: FASE 2

La Fase 2 implementara **Feature Engineering** con los siguientes modulos:

1. `hard_skills_scorer.py` - Similitud semantica con TF-IDF y Jaccard
2. `soft_skills_scorer.py` - Matching de habilidades blandas
3. `feature_extractor.py` - Orquestador que llama a los 5 scorers

Los modulos de Fase 1 seran utilizados por el feature_extractor para generar el vector de features completo del candidato.

---

## NOTAS TECNICAS

- Los archivos originales de la carpeta `ML/fase1/` usaban caracteres con tildes (ñ, á, é, etc.). En la implementacion se removieron las tildes para evitar problemas de encoding en diferentes sistemas.
- El resumen original (`FASE_1_RESUMEN.md`) mencionaba perfiles ficticios (tech_startup, gov_health), pero se implementaron los perfiles reales encontrados en los archivos JSON (AGETIC, Banco FIE, INTI, Empacar, MOPSV).
