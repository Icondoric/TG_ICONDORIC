import os
import json
import google.generativeai as genai
from typing import Dict, Any

# Configure API Key securely
def configure_genai():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found in environment variables.")
        return False
    genai.configure(api_key=api_key)
    return True

def extract_skills_with_llm(text: str) -> Dict[str, Any]:
    """
    Extracts skills and professional summary using Google Gemini.
    Returns a dictionary with 'skills' (list) and 'summary' (str).
    """
    if not configure_genai():
        return {"error": "API Key missing", "skills": [], "summary": ""}

    model = genai.GenerativeModel('gemini-flash-latest')

    prompt = f"""
    Actúa como un reclutador experto en tecnología y RRHH. Analiza el siguiente texto extraído de un CV y extrae la información relevante en un formato estructurado.
    
    TEXTO DEL CV:
    {text[:4000]}  # Limit text length

    Instrucciones:
    1. Extrae **Habilidades Técnicas** (Hard Skills) y **Habilidades Blandas** (Soft Skills).
    2. Extrae el **Historial Académico** (Education) con título, institución y año.
    3. Extrae la **Experiencia Laboral** (Experience) con cargo, empresa, duración y una breve descripción.
    4. Extrae los **Idiomas**.
    5. Redacta un **Breve Resumen Profesional** (máximo 3 líneas).
    
    Retorna SOLAMENTE un JSON válido con el siguiente formato:
    {{
        "personal_info": {{
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

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up potential markdown formatting like ```json ... ```
        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "").replace("```", "")
        
        data = json.loads(response_text)
        return data
    except Exception as e:
        print(f"Error extracting with Gemini: {e}")
        return {"error": str(e), "skills": [], "summary": ""}
