from typing import List, Dict, Set, Any
from .esco import esco_loader
from .nlp import clean_text, nlp
from spacy.tokens import Doc

# Initialize loader on module import (or lazy load when needed)
try:
    esco_loader.load_data()
except Exception as e:
    print(f"Failed to initialize ESCO loader: {e}")

def extract_skills(text: str, doc: Doc = None) -> Dict[str, Any]:
    """
    Extracts skills and occupations from text using ESCO dataset.
    Returns a structured dictionary with categorized findings.
    """
    # Ensure matcher is built (idempotent)
    esco_loader.build_matcher(nlp)

    # Use the cleaning function to normalize whitespace if no doc provided
    if not doc:
        cleaned_text = clean_text(text)
        doc = nlp(cleaned_text)
    
    # Use ESCOLoader to search for items using Spacy Matcher
    results = esco_loader.search_items_spacy(doc)
    
    # Format Skills
    # De-duplicate by label, but keep categories
    skills_output = []
    seen_skills = set()
    
    for skill in results["skills"]:
        if skill["label"] not in seen_skills:
            skills_output.append({
                "name": skill["label"],
                "categories": skill["categories"],
                "uri": skill["uri"]
            })
            seen_skills.add(skill["label"])
            
    # Format Occupations
    occupations_output = []
    seen_occupations = set()
    
    for occ in results["occupations"]:
        if occ["label"] not in seen_occupations:
            occupations_output.append({
                "name": occ["label"],
                "uri": occ["uri"]
            })
            seen_occupations.add(occ["label"])
    
    return {
        "skills": sorted(skills_output, key=lambda x: x["name"]),
        "occupations": sorted(occupations_output, key=lambda x: x["name"])
    }

