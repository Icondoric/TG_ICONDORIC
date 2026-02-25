import os
import json
import asyncio
import logging
import threading
from typing import Dict, Any, List

import google.generativeai as genai

from app.core.config import settings

logger = logging.getLogger(__name__)


# =============================================
# API Key Pool with automatic rotation
# =============================================

class GeminiKeyPool:
    """
    Pool de API keys de Gemini con rotacion automatica.

    Uso en .env:
        GEMINI_API_KEY=key1            (una sola key, como antes)
        GEMINI_API_KEYS=key1,key2,key3 (multiples keys separadas por coma)

    Si ambas existen, se combinan sin duplicados.
    Cuando una key da error 429 (quota), rota a la siguiente.
    """

    def __init__(self):
        self._keys: List[str] = []
        self._current_index = 0
        self._lock = threading.Lock()
        self._configured_key = None  # Track which key genai is currently using
        self._load_keys()

    def _load_keys(self):
        keys = set()

        # Single key (backward compat)
        single = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        if single.strip():
            keys.add(single.strip())

        # Multiple keys
        multi = os.getenv("GEMINI_API_KEYS", "")
        if multi.strip():
            for k in multi.split(","):
                k = k.strip()
                if k:
                    keys.add(k)

        self._keys = list(keys)
        if self._keys:
            logger.info(f"Gemini key pool: {len(self._keys)} key(s) loaded")
        else:
            logger.warning("No Gemini API keys found in environment")

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
            logger.info(f"Rotated Gemini key: slot {old_index} -> {self._current_index} (of {len(self._keys)})")
            return new_key

    def configure_current(self):
        """Configure genai with the current key (only if changed)."""
        key = self.get_current_key()
        if key and key != self._configured_key:
            genai.configure(api_key=key)
            self._configured_key = key


# Global key pool instance
_key_pool = GeminiKeyPool()

# Semaphore: max concurrent Gemini calls
MAX_CONCURRENT_GEMINI = int(os.getenv("MAX_CONCURRENT_GEMINI", "5"))
_gemini_semaphore = asyncio.Semaphore(MAX_CONCURRENT_GEMINI)

# Retry settings
MAX_RETRIES = settings.GEMINI_MAX_RETRIES  # default 3
GEMINI_TIMEOUT_SECONDS = int(os.getenv("GEMINI_TIMEOUT_SECONDS", "60"))

# Model (configurable via env)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def _build_prompt(text: str) -> str:
    return f"""
    Actúa como un reclutador experto en tecnología y RRHH. Analiza el siguiente texto extraído de un CV y extrae la información relevante en un formato estructurado.

    TEXTO DEL CV:
    {text[:4000]}

    Instrucciones:
    1. Extrae los **Datos Personales**: nombre completo, teléfono, email, ubicación/dirección y nacionalidad si están mencionados.
    2. Extrae **Habilidades Técnicas** (Hard Skills) y **Habilidades Blandas** (Soft Skills).
    3. Extrae el **Historial Académico** (Education) con título, institución y año.
    4. Extrae la **Experiencia Laboral** (Experience) con cargo, empresa, duración y una breve descripción.
    5. Extrae los **Idiomas**.
    6. Redacta un **Breve Resumen Profesional** (máximo 3 líneas).

    Retorna SOLAMENTE un JSON válido con el siguiente formato:
    {{
        "personal_info": {{
            "name": "Nombre Completo del candidato o null si no está",
            "phone": "Número de teléfono o null si no está",
            "email": "email@ejemplo.com o null si no está",
            "location": "Ciudad, País o null si no está",
            "nationality": "Nacionalidad o null si no está",
            "summary": "Resumen del perfil...",
            "languages": ["Inglés (B2)", "Español (Nativo)"]
        }},
        "hard_skills": ["Python", "React", "SQL"],
        "soft_skills": ["Liderazgo", "Comunicación"],
        "education": [
            {{
                "degree": "Título obtenido",
                "institution": "Nombre Universidad",
                "year": "2020"
            }}
        ],
        "experience": [
            {{
                "role": "Cargo desempeñado",
                "company": "Nombre Empresa",
                "duration": "2021 - Presente",
                "description": "Breve descripción de responsabilidades"
            }}
        ]
    }}
    """



def _parse_gemini_response(response_text: str) -> Dict[str, Any]:
    """Parse and clean Gemini response text into a dict."""
    text = response_text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


def _is_quota_error(error: Exception) -> bool:
    """Check if error is a 429 quota/rate-limit error."""
    err_str = str(error)
    return "429" in err_str or "quota" in err_str.lower() or "rate" in err_str.lower()


def _call_gemini_sync(prompt: str) -> Dict[str, Any]:
    """Synchronous Gemini call (runs inside thread executor)."""
    _key_pool.configure_current()
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    return _parse_gemini_response(response.text)


def extract_skills_with_llm_sync(text: str) -> Dict[str, Any]:
    """Sync wrapper for backward compat (used by deprecated nlp.py)."""
    if not _key_pool.has_keys:
        return {"error": "API Key missing", "skills": [], "summary": ""}
    prompt = _build_prompt(text)
    try:
        return _call_gemini_sync(prompt)
    except Exception as e:
        if _is_quota_error(e) and _key_pool.key_count > 1:
            _key_pool.rotate()
            _key_pool.configure_current()
            try:
                return _call_gemini_sync(prompt)
            except Exception as e2:
                logger.error(f"Sync Gemini extraction error after rotation: {e2}")
                return {"error": str(e2), "skills": [], "summary": ""}
        logger.error(f"Sync Gemini extraction error: {e}")
        return {"error": str(e), "skills": [], "summary": ""}


async def extract_skills_with_llm(text: str) -> Dict[str, Any]:
    """
    Extracts skills and professional info using Google Gemini.
    - Async: does not block the event loop
    - Semaphore: limits concurrent Gemini calls
    - Timeout: fails after GEMINI_TIMEOUT_SECONDS
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
            async with _gemini_semaphore:
                logger.info(f"Gemini attempt {attempt}/{MAX_RETRIES} (key slot {_key_pool._current_index})")
                loop = asyncio.get_event_loop()
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, _call_gemini_sync, prompt),
                    timeout=GEMINI_TIMEOUT_SECONDS
                )
                return result

        except asyncio.TimeoutError:
            last_error = f"Timeout after {GEMINI_TIMEOUT_SECONDS}s (attempt {attempt})"
            logger.warning(last_error)

        except json.JSONDecodeError as e:
            last_error = f"Invalid JSON from Gemini (attempt {attempt}): {e}"
            logger.warning(last_error)

        except Exception as e:
            last_error = f"Gemini error (attempt {attempt}): {e}"
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

    logger.error(f"Gemini extraction failed after {MAX_RETRIES} attempts: {last_error}")
    return {"error": last_error, "skills": [], "summary": ""}
