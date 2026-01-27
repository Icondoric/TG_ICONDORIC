import re
import spacy
from .llm_extractor import extract_skills_with_llm

def load_spacy_model():
    try:
        return spacy.load("es_core_news_sm")
    except OSError:
        print("Warning: es_core_news_sm not found. Using blank 'es' model.")
        return spacy.blank("es")

nlp = load_spacy_model()

def clean_text(text: str) -> str:
    """
    Cleans and normalizes text by removing extra whitespace and 
    stripping leading/trailing spaces.
    """
    if not text:
        return ""
    
    # Replace multiple whitespace characters with a single space
    cleaned_text = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing whitespace
    return cleaned_text.strip()



def extract_emails(text: str) -> list:
    """Extract email addresses using regex."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return list(set(re.findall(email_pattern, text)))

def extract_phone_numbers(text: str) -> list:
    """
    Extract phone numbers with strict filtering to avoid dates/indices.
    """
    # General pattern: Optional Country Code (+34, +51) + Blocks of digits
    # Must be at least 8 digits long.
    # Matches formats like: +34 600 000 000, 600-000-000, 600 000 000, or 8 consecutive digits
    phone_pattern = r'(?:\+?\d{1,3}[ -]?)?(?:[679]\d{2}[ -]?\d{3}[ -]?\d{3}|\b\d{3}[ -]?\d{2}[ -]?\d{2}[ -]?\d{2}\b|\b\d{4}[ -]?\d{4}\b|\b\d{8}\b)'
    
    matches = re.findall(phone_pattern, text)
    valid_phones = []
    for m in matches:
        # Cleanup
        clean_p = re.sub(r'\D', '', m)
        
        # Length check (7 to 15 digits)
        if not (7 <= len(clean_p) <= 15):
            continue
            
        # Anti-Date/Year Heuristics
        # 1. Single Year: If it looks like a year 1990-2030 standing alone (4 digits), ignore (covered by length check > 7, but just in case logic changes)
        
        # 2. Date Ranges (e.g. 2017-2019, 1990-2000). Total digits = 8.
        if len(clean_p) == 8:
            # Check if it starts with 19 or 20 (common centuries)
            if clean_p.startswith('19') or clean_p.startswith('20'):
                # Check for separator structure
                # If the match has a separator in the middle, likely a date range
                # Regex to split: 2017-2019 -> ['2017', '2019']
                parts = re.split(r'\D+', m)
                parts = [p for p in parts if p] # filter empty
                
                # If we have 2 parts of 4 digits, and both look like years
                if len(parts) == 2 and len(parts[0]) == 4 and len(parts[1]) == 4:
                     p1, p2 = int(parts[0]), int(parts[1])
                     if (1900 <= p1 <= 2100) and (1900 <= p2 <= 2100):
                         continue

        valid_phones.append(m.strip())
            
    return list(set(valid_phones))

def extract_careers(text: str) -> list:
    """
    Extract potential degrees/careers using Regex patterns and expanded Keywords.
    """
    careers = []
    cleaned_text = re.sub(r'\s+', ' ', text) # Single line for easier regex

    # 1. Regex Patterns for precise titles
    patterns = [
        r'(?i)(?:Ingenier[ía|o]|Licenciatur[a|o]|Grado|Diplomatura|Técnic[o|a]|Máster|Doctorado) (?:en|de) [a-zA-ZáéíóúÁÉÍÓÚñÑ ]+',
        r'(?i)(?:Arquitect[o|ura]|Psicólog[o|ía]|Abogad[o|a])'
    ]
    
    for pat in patterns:
        matches = re.findall(pat, cleaned_text)
        for m in matches:
            # Filter out too long phrases (false positives capturing whole paragraphs)
            if len(m.split()) <= 6: 
                careers.append(m.strip())

    # 2. Keyword fallback (if regex didn't catch specific "Administrador")
    keywords = [
        "Analista de Sistemas", "Desarrollador Full Stack", "Project Manager",
        "Contador Público", "Economista", "Administrador de Empresas",
        "Enfermero", "Médico Cirujano", "Marketing Digital", "Community Manager",
        "Diseñador Gráfico", "Diseño Gráfico", "Consultor", "Auditor", "Psicólogo Organizacional",
        "Recursos Humanos", "Ventas", "Atención al Cliente", "Soporte Técnico"
    ]
    
    for k in keywords:
        # Case insensitive search for keywords
        if re.search(r'\b' + re.escape(k) + r'\b', cleaned_text, re.IGNORECASE):
            careers.append(k)

    return list(set(careers))

def segment_cv(text: str) -> dict:
    """
    Segment CV into sections based on heuristic keywords.
    """
    segments = {
        "personal_info": "",
        "experience": "",
        "education": "",
        "skills": "",
        "other": ""
    }
    
    # Simple keyword-based segmentation
    lower_text = text.lower()
    lines = text.split('\n')
    
    current_section = "personal_info" # Default start
    
    # Keywords to trigger section change
    section_map = {
        "experiencia": "experience",
        "laboral": "experience",
        "trayectoria": "experience",
        "educación": "education",
        "formación": "education",
        "estudios": "education",
        "académica": "education",
        "habilidades": "skills",
        "competencias": "skills",
        "conocimientos": "skills",
        "skills": "skills",
        "idiomas": "skills",
        "proyectos": "other",
        "referencias": "other"
    }
    
    buffer = []
    
    for line in lines:
        clean_line = line.strip().lower()
        
        # Check if line is a likely header (short, contains keyword)
        if len(clean_line) < 40:
            found_section = None
            for key, sec in section_map.items():
                if key in clean_line:
                    found_section = sec
                    break
            
            if found_section:
                # Save buffer to current section
                if buffer:
                    segments[current_section] += "\n".join(buffer) + "\n"
                    buffer = []
                current_section = found_section
                continue # Don't add header to body
                
        buffer.append(line)
        
    # Flush last buffer
    if buffer:
        segments[current_section] += "\n".join(buffer)
        
    return segments

def process_cv_text(text: str) -> dict:
    """
    Process CV text using spaCy and Custom Regex logic.
    Now includes Segmentation and Text Cleaning.
    """
    cleaned_text = clean_text(text)
    doc = nlp(cleaned_text) # Process the cleaned text
    
    entities = {}
    
    # 1. SpaCy NER (Basic entities)
    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = []
        if ent.text not in entities[ent.label_]:
            entities[ent.label_].append(ent.text)
            
    # 2. Text Segmentation (New)
    segments = segment_cv(cleaned_text)
    
    # 3. Custom Regex Extraction
    
    # EMails 
    custom_emails = extract_emails(cleaned_text)
    if custom_emails:
        entities['EMAIL'] = custom_emails
        
    # Phones (Strict)
    custom_phones = extract_phone_numbers(cleaned_text)
    if custom_phones:
        entities['PHONE'] = custom_phones
        
    # Careers/Titles
    # Improvement: Search in 'education' segment if available, else full text
    search_scope_careers = segments['education'] + "\n" + segments['personal_info'] if segments['education'] else cleaned_text
    custom_careers = extract_careers(search_scope_careers)
    
    if custom_careers:
        entities['CAREERS'] = custom_careers

    # 4. LLM Extraction (Gemini)
    try:
        llm_data = extract_skills_with_llm(cleaned_text)
        if "error" not in llm_data:
            entities['LLM_SKILLS'] = llm_data
    except Exception as e:
        print(f"LLM Extraction failed: {e}")
            
    return {
        "entities": entities,
        "segments": segments,
        "text_summary": cleaned_text[:300]
    }

