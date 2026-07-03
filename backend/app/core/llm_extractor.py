import os
import json
import asyncio
import logging
import threading
from typing import Dict, Any, List

#import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

load_dotenv(override=True)
# =============================================
# API Key Pool with automatic rotation
# =============================================

class OpenAIKeyPool:
    """
    Pool de API keys de OpenAI con rotacion automatica.

    Uso en .env:
        OPENAI_API_KEY=key1            (una sola key)
        OPENAI_API_KEYS=key1,key2,key3 (multiples keys separadas por coma)

    Si ambas existen, se combinan sin duplicados.
    Cuando una key da error 429 (quota), rota a la siguiente.
    """

    def __init__(self):
        self._keys: List[str] = []
        self._current_index = 0
        self._lock = threading.Lock()
        self._load_keys()

    def _load_keys(self):
        seen = set()
        keys = []

        # Multiple keys take priority (ordered)
        multi = os.getenv("OPENAI_API_KEYS", "")
        if multi.strip():
            for k in multi.split(","):
                k = k.strip()
                if k and k not in seen:
                    seen.add(k)
                    keys.append(k)

        # Single key (backward compat) — append if not already in list
        single = getattr(settings, "OPENAI_API_KEY", getattr(settings, "GEMINI_API_KEY", "")) or os.getenv("OPENAI_API_KEY", "")
        if single.strip() and single.strip() not in seen:
            keys.append(single.strip())

        self._keys = keys
        if self._keys:
            logger.info(f"OpenAI key pool: {len(self._keys)} key(s) loaded")
        else:
            logger.warning("No OpenAI API keys found in environment")

    @property
    def has_keys(self) -> bool:
        return len(self._keys) > 0

    @property
    def key_count(self) -> int:
        return len(self._keys)

    def get_current_key(self) -> str:
        """Get current active key."""
        if not self._keys:
            return ""
        return self._keys[self._current_index % len(self._keys)]

    def rotate(self) -> str:
        """Rotate to next key. Returns the new active key."""
        with self._lock:
            if len(self._keys) <= 1:
                return self.get_current_key()
            old_index = self._current_index
            self._current_index = (self._current_index + 1) % len(self._keys)
            new_key = self._keys[self._current_index]
            logger.info(f"Rotated OpenAI key: slot {old_index} -> {self._current_index} (of {len(self._keys)})")
            return new_key

# Global key pool instance
_key_pool = OpenAIKeyPool()

# Semaphore: max concurrent OpenAI calls
MAX_CONCURRENT_OPENAI = int(os.getenv("MAX_CONCURRENT_OPENAI", "5"))
_openai_semaphore = asyncio.Semaphore(MAX_CONCURRENT_OPENAI)

# Retry settings
MAX_RETRIES = getattr(settings, "OPENAI_MAX_RETRIES", getattr(settings, "GEMINI_MAX_RETRIES", 3))
OPENAI_TIMEOUT_SECONDS = int(os.getenv("OPENAI_TIMEOUT_SECONDS", "60"))

# Model (configurable via env)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def _build_prompt(text: str) -> str:
    return f"""
    Eres un sistema experto de análisis de currículums vitae (CV). Tu tarea es extraer TODA la información relevante del texto proporcionado con la máxima precisión posible.

    REGLAS CRÍTICAS (sin excepción):
    - Devuelve ÚNICAMENTE JSON válido. Sin texto adicional, sin bloques markdown, sin explicaciones.
    - Lee el CV COMPLETO de principio a fin antes de responder, incluso si está desordenado.
    - Si un campo no aparece en el CV, usa null para strings o [] para listas. NUNCA omitas un campo.
    - EXTRAE TODAS las habilidades e idiomas encontrados. No pongas límite de cantidad.
    - El CV puede estar desorganizado, sin secciones claras o con información mezclada: igualmente
      debes identificar y estructurar TODA la información relevante dondequiera que aparezca.

    TEXTO DEL CV:
    {text}

    ── INSTRUCCIÓN 1: DATOS PERSONALES ──
    Extrae: nombre completo, teléfono, email, ciudad/país, nacionalidad.

    ── INSTRUCCIÓN 2: HABILIDADES TÉCNICAS (hard_skills) ──
    FUENTES DE BÚSQUEDA — escanea TODAS sin excepción:
    a) Secciones explícitas: "Habilidades", "Skills", "Conocimientos", "Herramientas",
       "Tecnologías", "Competencias Técnicas", "Aptitudes", "Capacidades".
    b) Descripciones de experiencia laboral: si dice "desarrollé en Python" → extrae "Python".
    c) Proyectos: si dice "proyecto con React y MongoDB" → extrae "React" y "MongoDB".
    d) CURSOS Y CERTIFICACIONES (muy importante): si dice "Curso de Java", "Certificación AWS",
       "Diplomado en Power BI", "Taller de Excel avanzado", "Bootcamp de Data Science" →
       extrae el TEMA del curso como habilidad técnica (Java, AWS, Power BI, Excel, Python, etc.).
       También si dice "estudiando Python" o "en proceso de certificación en Docker" → extrae la habilidad.
    e) Logros y actividades: si se describe el uso de una herramienta aunque sea brevemente → extráela.

    Categorías a incluir:
    - Lenguajes: Python, Java, JavaScript, TypeScript, C++, C#, PHP, R, MATLAB, VBA, Kotlin, Swift, etc.
    - Frameworks/Librerías: React, Angular, Vue, Django, Flask, FastAPI, Spring, Node.js, .NET, Laravel, etc.
    - Bases de datos: SQL, MySQL, PostgreSQL, MongoDB, Oracle, SQLite, Redis, Firebase, etc.
    - Cloud/DevOps: Docker, Kubernetes, AWS, Azure, GCP, Git, GitHub, CI/CD, Linux, Terraform, etc.
    - Software: AutoCAD, SAP, Excel, Power BI, Tableau, SPSS, Figma, Photoshop, Word, etc.
    - Metodologías: Scrum, Agile, Kanban, PMBOK, ITIL, Lean, Six Sigma, etc.
    - Otros: cualquier tecnología, herramienta o conocimiento técnico/científico mencionado.

    Formato: lista de strings cortos y precisos, ej: ["Python", "React", "PostgreSQL", "Docker"]

    ── INSTRUCCIÓN 3: HABILIDADES BLANDAS (soft_skills) ──
    FUENTES DE BÚSQUEDA — escanea TODAS sin excepción:
    a) Secciones explícitas: "Habilidades Blandas", "Soft Skills", "Competencias", "Perfil".
    b) Descripción personal o perfil profesional al inicio del CV.
    c) Descripciones de experiencia laboral: si dice "lideré un equipo" → extrae "Liderazgo";
       "coordiné reuniones" → "Comunicación efectiva"; "resolví conflictos" → "Resolución de conflictos".
    d) CURSOS Y CERTIFICACIONES: si dice "Curso de Liderazgo", "Taller de Comunicación Efectiva",
       "Diplomado en Gestión de Equipos", "Capacitación en Servicio al Cliente" →
       extrae la habilidad blanda del tema del curso.
    e) Logros que impliquen competencias: "aumenté ventas coordinando equipo" → "Liderazgo", "Orientación a resultados".
    f) Actividades extracurriculares o voluntariado que evidencien habilidades sociales.

    Categorías a detectar (y sus sinónimos/variantes):
    - Comunicación: comunicación efectiva, asertiva, presentaciones, oratoria, redacción
    - Liderazgo: gestión de equipos, dirección, supervisión, mentoría
    - Trabajo en equipo: colaboración, trabajo colaborativo, sinergia
    - Resolución de problemas: pensamiento analítico, toma de decisiones, pensamiento crítico
    - Adaptabilidad: flexibilidad, apertura al cambio, resiliencia, polivalencia
    - Organización: gestión del tiempo, planificación, priorización, multitarea
    - Orientación a resultados: enfoque en metas, cumplimiento de objetivos, proactividad
    - Creatividad: innovación, pensamiento creativo, generación de ideas
    - Inteligencia emocional: empatía, manejo del estrés, autocontrol, relaciones interpersonales
    - Ética y responsabilidad: compromiso, puntualidad, responsabilidad, integridad
    - Servicio al cliente, negociación, persuasión, ventas consultivas

    Normaliza a forma corta y clara: "Liderazgo" en vez de "Capacidad para liderar equipos de trabajo".
    Formato: lista de strings, ej: ["Liderazgo", "Trabajo en equipo", "Comunicación efectiva"]

    ── INSTRUCCIÓN 4: IDIOMAS (languages) — FORMATO OBLIGATORIO ──
    Busca en TODO el texto cualquier idioma/lengua mencionado (secciones "Idiomas", "Languages",
    dentro de habilidades, dentro de experiencias, etc.).
    REGLA DE FORMATO: cada idioma DEBE seguir el patrón: "NombreIdioma (Nivel)"
    Donde el nivel DEBE ser uno de los siguientes valores exactos del Marco Europeo (CEFR):
      A1, A2, B1, B2, C1, C2, Nativo, Materno, Básico, Intermedio, Avanzado, Fluido
    Conversión de términos comunes:
      - "native" / "nativo" / "materno"            → Nativo
      - "basic" / "básico" / "elemental"            → Básico
      - "intermediate" / "intermedio"               → Intermedio
      - "advanced" / "avanzado" / "fluent" / "fluido" → Avanzado
      - Niveles CEFR literales (A1, A2, B1, B2, C1, C2) → úsalos tal cual
      - Sin nivel especificado                      → omite el paréntesis (ej: "Inglés")
    Traduce el nombre del idioma al español:
      English → Inglés | Français → Francés | Deutsch → Alemán | Português → Portugués
    Ejemplos correctos: ["Español (Nativo)", "Inglés (B2)", "Francés (Intermedio)", "Alemán (A2)"]
    Ejemplos INCORRECTOS (no uses): ["English Advanced", "Inglés avanzado", "Español - nativo"]

    ── INSTRUCCIÓN 5: EDUCACIÓN ──
    Extrae cada título académico: título/grado, institución y año (o período).

    ── INSTRUCCIÓN 6: EXPERIENCIA LABORAL ──
    Extrae cada experiencia: cargo, empresa, período y descripción breve de responsabilidades.

    ── INSTRUCCIÓN 7: RESUMEN PROFESIONAL ──
    Redacta un resumen conciso (máximo 3 líneas) basado en el perfil real del candidato.

    ESTRUCTURA JSON DE RESPUESTA (devuelve EXACTAMENTE esto, sin campos adicionales):
    {{
        "personal_info": {{
            "name": "Nombre Completo o null",
            "phone": "Teléfono o null",
            "email": "correo@ejemplo.com o null",
            "location": "Ciudad, País o null",
            "nationality": "Nacionalidad o null",
            "summary": "Resumen profesional...",
            "languages": ["Español (Nativo)", "Inglés (B2)"]
        }},
        "hard_skills": ["Python", "React", "SQL"],
        "soft_skills": ["Liderazgo", "Trabajo en equipo"],
        "education": [
            {{
                "degree": "Título obtenido",
                "institution": "Nombre institución",
                "year": "2020"
            }}
        ],
        "experience": [
            {{
                "role": "Cargo",
                "company": "Empresa",
                "duration": "2021 - Presente",
                "description": "Descripción de responsabilidades"
            }}
        ]
    }}
    """



def _build_oferta_prompt(text: str) -> str:
    return f"""
    Eres un sistema experto en Recursos Humanos. Analiza el siguiente texto de una convocatoria laboral y extrae toda la información relevante.
    Devuelve ÚNICAMENTE JSON válido, sin texto adicional ni bloques markdown.

    TEXTO DE LA OFERTA:
    {text}

    Instrucciones:
    1. Extrae el **título del puesto** (campo "titulo").
    2. Extrae la **descripción** o resumen de funciones/responsabilidades (campo "descripcion", máximo 2000 caracteres).
    3. Extrae la **ubicación** o ciudad (campo "ubicacion").
    4. Extrae el **área** o sector laboral (ej. "Tecnología", "Finanzas", "Ingeniería Civil") (campo "area").
    5. Determina el **tipo**: "pasantia" si es práctica/pasantía/internado para estudiantes, "empleo" si es trabajo para titulados/profesionales. Si no queda claro, pon null.
    6. Determina la **modalidad**: "presencial", "remoto" o "hibrido". Si no se menciona, pon null.
    7. Extrae la **fecha de cierre** de postulación en formato YYYY-MM-DD (campo "fecha_cierre"). Si no se menciona, pon null.
    8. Extrae el **número de vacantes** disponibles (campo "cupos_disponibles", entero). Si no se menciona, pon null.
    9. Extrae el **teléfono de contacto** (campo "contact_phone"). Si no se menciona, pon null.
    10. Extrae el **email de contacto** (campo "contact_email"). Si no se menciona, pon null.
    11. Extrae las **habilidades técnicas requeridas** (campo "required_skills", lista de strings). Solo las mencionadas explícitamente.
    12. Extrae las **habilidades blandas requeridas** (campo "required_soft_skills", lista de strings).
    13. Extrae los **idiomas requeridos** (campo "required_languages", lista de strings, ej. "Español", "Inglés").
    14. Determina el **nivel educativo mínimo requerido** (campo "required_education_level"). Debe ser exactamente uno de: "Bachillerato", "Tecnico", "Licenciatura", "Ingenieria", "Maestria", "Doctorado". Si no se especifica, pon null.
    15. Extrae los **años mínimos de experiencia** requeridos (campo "min_experience_years", número decimal). Si no se menciona, pon null.
    16. Si la oferta menciona carreras específicas aceptadas, extrae solo las que coincidan con esta lista exacta (campo "carreras_aceptadas"): ["Ingenieria Civil", "Ingenieria de Sistemas", "Ingenieria Geografica", "Ingenieria Mecatronica", "Ingenieria en Sistemas Electronicos", "Ingenieria Financiera", "Ingenieria Industrial", "Derecho", "Ingenieria Comercial"]. Si no se mencionan carreras específicas, devuelve lista vacía [].
    17. Si es pasantía y se menciona semestre mínimo requerido, extrae "semestre_minimo" (entero 1-10). Si no, pon null.
    18. Si es pasantía y se menciona semestre máximo, extrae "semestre_maximo" (entero 1-10). Si no, pon null.

    Retorna SOLAMENTE un JSON válido con este formato exacto:
    {{
        "titulo": "Nombre del puesto o null",
        "descripcion": "Descripción de funciones o null",
        "ubicacion": "Ciudad/País o null",
        "area": "Área laboral o null",
        "tipo": "pasantia" | "empleo" | null,
        "modalidad": "presencial" | "remoto" | "hibrido" | null,
        "fecha_cierre": "YYYY-MM-DD o null",
        "cupos_disponibles": 1,
        "contact_phone": "teléfono o null",
        "contact_email": "email o null",
        "required_skills": ["skill1", "skill2"],
        "required_soft_skills": ["soft1"],
        "required_languages": ["Español", "Inglés"],
        "required_education_level": "Licenciatura" | null,
        "min_experience_years": 2.0 | null,
        "carreras_aceptadas": [],
        "semestre_minimo": null,
        "semestre_maximo": null
    }}
    """


def _parse_llm_response(response_text: str) -> Dict[str, Any]:
    """Parse and clean LLM response text into a dict."""
    text = response_text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


def _is_quota_error(error: Exception) -> bool:
    """Check if error is a 429 quota/rate-limit error."""
    err_str = str(error)
    return "429" in err_str or "quota" in err_str.lower() or "rate" in err_str.lower() or "insufficient_quota" in err_str.lower()


def _call_openai_sync(prompt: str) -> Dict[str, Any]:
    """Synchronous OpenAI call (runs inside thread executor)."""
    api_key = _key_pool.get_current_key()
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{'role':'system','content':prompt}]
    )
    return _parse_llm_response(response.choices[0].message.content)


def extract_skills_with_llm_sync(text: str) -> Dict[str, Any]:
    """Sync wrapper for backward compat (used by deprecated nlp.py)."""
    if not _key_pool.has_keys:
        return {"error": "API Key missing", "skills": [], "summary": ""}
    prompt = _build_prompt(text)
    try:
        return _call_openai_sync(prompt)
    except Exception as e:
        if _is_quota_error(e) and _key_pool.key_count > 1:
            _key_pool.rotate()
            try:
                return _call_openai_sync(prompt)
            except Exception as e2:
                logger.error(f"Sync OpenAI extraction error after rotation: {e2}")
                return {"error": str(e2), "skills": [], "summary": ""}
        logger.error(f"Sync OpenAI extraction error: {e}")
        return {"error": str(e), "skills": [], "summary": ""}


async def extract_skills_with_llm(text: str) -> Dict[str, Any]:
    """
    Extracts skills and professional info using OpenAI.
    - Async: does not block the event loop
    - Semaphore: limits concurrent OpenAI calls
    - Timeout: fails after OPENAI_TIMEOUT_SECONDS
    - Retries: up to MAX_RETRIES with exponential backoff
    - Key rotation: on 429 errors, rotates to next API key
    """
    if not _key_pool.has_keys:
        return {"error": "API Key missing", "skills": [], "summary": ""}

    prompt = _build_prompt(text)
    last_error = None
    keys_tried = 0

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with _openai_semaphore:
                logger.info(f"OpenAI attempt {attempt}/{MAX_RETRIES} (key slot {_key_pool._current_index})")
                loop = asyncio.get_event_loop()
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, _call_openai_sync, prompt),
                    timeout=OPENAI_TIMEOUT_SECONDS
                )
                return result

        except asyncio.TimeoutError:
            last_error = f"Timeout after {OPENAI_TIMEOUT_SECONDS}s (attempt {attempt})"
            logger.warning(last_error)

        except json.JSONDecodeError as e:
            last_error = f"Invalid JSON from OpenAI (attempt {attempt}): {e}"
            logger.warning(last_error)

        except Exception as e:
            last_error = f"OpenAI error (attempt {attempt}): {e}"
            logger.warning(last_error)

            # On quota error: rotate key immediately
            if _is_quota_error(e) and _key_pool.key_count > 1:
                keys_tried += 1
                if keys_tried < _key_pool.key_count:
                    _key_pool.rotate()
                    logger.info(f"Quota hit - rotated to key slot {_key_pool._current_index}")
                    # Retry immediately with new key (no backoff)
                    continue
                else:
                    logger.error("All API keys exhausted (quota on all)")

        # Exponential backoff before retry
        if attempt < MAX_RETRIES:
            wait = 2 ** (attempt - 1)
            logger.info(f"Retrying in {wait}s...")
            await asyncio.sleep(wait)

    logger.error(f"OpenAI extraction failed after {MAX_RETRIES} attempts: {last_error}")
    return {"error": last_error, "skills": [], "summary": ""}


async def extract_oferta_with_llm(text: str) -> Dict[str, Any]:
    """
    Extrae información estructurada de una convocatoria laboral usando OpenAI.
    Mismo mecanismo que extract_skills_with_llm (semáforo, reintentos, rotación de keys).
    """
    if not _key_pool.has_keys:
        return {"error": "API Key missing"}

    prompt = _build_oferta_prompt(text)
    last_error = None
    keys_tried = 0

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with _openai_semaphore:
                logger.info(f"OpenAI oferta attempt {attempt}/{MAX_RETRIES} (key slot {_key_pool._current_index})")
                loop = asyncio.get_event_loop()
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, _call_openai_sync, prompt),
                    timeout=OPENAI_TIMEOUT_SECONDS
                )
                return result

        except asyncio.TimeoutError:
            last_error = f"Timeout after {OPENAI_TIMEOUT_SECONDS}s (attempt {attempt})"
            logger.warning(last_error)

        except json.JSONDecodeError as e:
            last_error = f"Invalid JSON from OpenAI (attempt {attempt}): {e}"
            logger.warning(last_error)

        except Exception as e:
            last_error = f"OpenAI error (attempt {attempt}): {e}"
            logger.warning(last_error)
            if _is_quota_error(e) and _key_pool.key_count > 1:
                keys_tried += 1
                if keys_tried < _key_pool.key_count:
                    _key_pool.rotate()
                    continue

        if attempt < MAX_RETRIES:
            await asyncio.sleep(2 ** (attempt - 1))

    logger.error(f"Oferta extraction failed after {MAX_RETRIES} attempts: {last_error}")
    return {"error": last_error}
