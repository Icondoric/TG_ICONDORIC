from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core import nlp, skills
import pdfplumber
import io

router = APIRouter()

@router.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")
    
    try:
        contents = await file.read()
        
        text = ""
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        if not text.strip():
             raise HTTPException(status_code=400, detail="Could not extract text from PDF. It might be an image scan.")

        # Process with NLP
        nlp_data = nlp.process_cv_text(text)
        entities = nlp_data.get("entities", {})
        
        # Extract Skills and Occupations
        extraction_result = skills.extract_skills(text)
        
        return {
            "message": "CV processed successfully",
            "data": {
                "personal_info": {
                    "email": entities.get("EMAIL", [""])[0] if entities.get("EMAIL") else "",
                    "phone": entities.get("PHONE", [""])[0] if entities.get("PHONE") else "",
                    "detected_names": entities.get("PER", []),
                    "degree": entities.get("CAREERS", [""])[0] if entities.get("CAREERS") else ""
                },
                "skills": extraction_result["skills"],
                "occupations": extraction_result["occupations"],
                "education": nlp_data.get("segments", {}).get("education", ""), 
            },
             "raw_text_preview": text[:500] + "..." # Limit preview
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
