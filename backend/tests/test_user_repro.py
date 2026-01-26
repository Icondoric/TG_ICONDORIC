import sys
import os

# Add app to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core import nlp, skills

def test_user_case():
    text = """
    ESTEFANI VANIA FLORES TORREZ ESTUDIANTE DE INGENIERÍA COMERCIAL +591 65113003 
    estefani01torrez01@gmail.com Estudiante de Ingeniería Comercial, cursando mi 4to año en 
    la carrera, altamente motivada y orientada a los resultados, con fuertes habilidades 
    analíticas y capacidad para resolver problemas. Con aspiración de obtener experiencia 
    laboral aplicando mis conocimientos teóricos y habilidades prácticas, mientras continúo 
    aprendiendo y desarrollándome profesionalmente en un entorno empresarial dinámico, 
    estoy dispuesta a asumir nuevos desafíos y trabajar en equipo para lograr resultados 
    exitosos. EDUCACIÓN INGENIERÍA COMERCIAL Escuela Militar de Ingeniería-UALP 2020 - 
    Actualidad BACHILLER EN HUMANIDADES Col. Part. Nueva Jerusalén 2017-2019 CURSOS 
    RELIZADOS Participación en el foro debate PANORAMA ECONÓMICO 2023 realizado el 26 de 
    mayo 2023 Participación en los foros y exposiciones en las 1ras. JORNADAS EMPRESARIALES 
    EMI-2023 con carga horaria de 20 horas académicas.(1 y 2 junio 2023) Participación en la 
    presentación del DOSSIER DE ESTADISTICAS SOCIALES ECONOMICAS realizado el 12 de 
    noviembre del 2023 Participación en la BOLSA BOLIVIANA DE VALORES en la gestión II-2023 
    Participación en JORNADA MONETARIA XVI realizadon de 21 de junio EXPERIENCIA 
    Coordinadora del seminario de UDAPE Ejecutiva de ventas de Yanbal Ejecutiva en ventas y 
    marketing del emprendimiento bueno bonito barato (BBB) APTITUDES Compromiso 
    Responsabilidad Trabajo en equipo Aprendizaje continuo Motivación SOFTWARE Excel Word 
    Stata Power point Eviews IDIOMAS Español Inglés
    """
    
    print("--- Extracting Skills ---")
    res = skills.extract_skills(text)
    found_skills = [s['name'] for s in res['skills']]
    found_occupations = [o['name'] for o in res['occupations']]
    
    print("Found Skills:", found_skills)
    print("Found Occupations:", found_occupations)
    
    if "Panorama" in found_skills:
        print("FAIL: 'Panorama' found (False Positive)")
    else:
        print("PASS: 'Panorama' NOT found")

    if any("textil" in s.lower() for s in found_skills):
        print("FAIL: 'textil' related skill found")
    else:
        print("PASS: No 'textil' skills found")

if __name__ == "__main__":
    test_user_case()
