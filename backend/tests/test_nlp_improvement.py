import sys
import os

# Add app to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core import nlp
from app.core.nlp import segment_cv

def test_nlp_improvements():
    print("=== Testing NLP Improvements ===")


    # 2. Test Phone Strictness
    print("\n[Test 2] Phone Extraction (Strictness)")
    text_phones = "Mi teléfono es 600 123 456. Trabajé en 2020-2021. ID: 12345678."
    # Expect: 600 123 456. NOT 20202021, NOT 12345678.
    
    res_nlp = nlp.process_cv_text(text_phones)
    phones = res_nlp['entities'].get('PHONE', [])
    print(f"Input: '{text_phones}'")
    print(f"Extracted Phones: {phones}")
    
    if len(phones) == 1 and "600 123 456" in phones[0]: # Regex might keep spaces or not depending on implementation
        print("PASS: Only extracted valid phone.")
    elif len(phones) > 1:
        print("FAIL: Too many phones extracted (likely dates).")
    else:
        print("FAIL: No phone extracted.")

    # 3. Test Segmentation & Degree in Context
    print("\n[Test 3] Segmentation & Degree Extraction")
    text_seg = """
    DATOS PERSONALES
    Juan Perez
    
    EDUCACIÓN
    Ingeniero de Sistemas - Univ X
    
    EXPERIENCIA
    Pizzeria - Cocinero
    """
    res_seg = nlp.process_cv_text(text_seg)
    degrees = res_seg['entities'].get('CAREERS', [])
    segments = res_seg.get('segments', {})
    
    print(f"Extracted Degree: {degrees}")
    print(f"Education Segment: '{segments.get('education', '').strip()}'")
    
    if "Ingeniero de Sistemas" in degrees and segments.get('education'):
        print("PASS: Degree extracted from Education section.")
    else:
        print("FAIL: Degree miss or segmentation fail.")

if __name__ == "__main__":
    test_nlp_improvements()
