from app.core.llm_extractor import extract_skills_with_llm
from dotenv import load_dotenv
import os
import sys

# Load env to ensure key is present
load_dotenv(".env")

sample_text = """
Desarrollador Full Stack Senior
Resumen: Apasionado por el código limpio.
Experiencia:
- Tech Lead en Google (2020-Presente): Lideré equipo de 5 personas.
- Junior Dev en Startup X (2018-2019): Mantenimiento de API.
Educación:
- Ingeniero de Sistemas, UNAM (2017).
Habilidades: Python, React.
Idiomas: Inglés Avanzado.
"""

print("--- START VERIFICATION ---")
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key Present: {bool(api_key)}")
if api_key:
    # Print first few chars to verify it's loaded correct (safe enough for debug)
    print(f"API Key start: {api_key[:5]}...")

result = extract_skills_with_llm(sample_text)
print("\n--- RAW RESULT ---")
print(result)

if "error" in result:
    print("\n[FAILED] Error returned:")
    print(result["error"])
    sys.exit(1)

if not result.get("hard_skills") and not result.get("soft_skills"):
    print("\n[WARNING] No skills extracted. Check model response.")
else:
    print("\n[SUCCESS] Extraction successful.")
    print("Keys found:", list(result.keys()))
    if "education" in result:
        print(f"Education items: {len(result['education'])}")
    if "experience" in result:
        print(f"Experience items: {len(result['experience'])}")
