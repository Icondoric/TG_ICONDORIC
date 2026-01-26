import sys
import os

# Add app to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core import skills, nlp

def test_systemic_filters():
    print("=== Testing Systemic POS & Entity Filters ===")
    
    # Case 1: Verbs acting as skills (False Positives)
    # "Plan" is a skill in ESCO? Maybe not, but "Design" is. "Go" is.
    # Sentence: "I plan to go home." -> Should match nothing.
    text_verb = "Yo suelo ir a casa."
    res_verb = skills.extract_skills(text_verb)
    print(f"\n[Test 1] Verbs ('ir' -> 'Go', 'suelo' -> 'Ground'?)\nInput: '{text_verb}'")
    print("Found:", [s['name'] for s in res_verb['skills']])
    
    # "Go" as a skill
    text_skill = "Soy experto en el lenguaje Go y R."
    res_skill = skills.extract_skills(text_skill)
    print(f"\n[Test 2] Real Skills ('Go', 'R')\nInput: '{text_skill}'")
    print("Found:", [s['name'] for s in res_skill['skills']])
    
    # Case 2: Entity Overlap
    # "Jordan" might be a skill/place?
    # "Paris" might be a tool?
    # Let's try something we know: "Amazon" (Company vs Cloud)
    # Or "Java" (Island vs Language) - Spacy might say Java is LOC if context is "I went to Java, Indonesia".
    
    text_entity = "Michael Jordan jugó baloncesto." 
    # If "Jordan" is a skill in our DB, it shouldn't match here because it's inside PER entity.
    res_ent = skills.extract_skills(text_entity)
    print(f"\n[Test 3] Entity Overlap ('Michael Jordan')\nInput: '{text_entity}'")
    print("Found:", [s['name'] for s in res_ent['skills']])

if __name__ == "__main__":
    test_systemic_filters()
