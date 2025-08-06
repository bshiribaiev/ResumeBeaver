# tools/api_helpers.py
from .pdf_parser import extract_text_from_pdf
from .docx_parser import extract_text_from_docx
from .text_cleaner import clean_text
from .match_score import compute_match_score

def enhanced_file_processing(file_path: str, file_type: str):
    """Enhanced processing for Arsenii's upload endpoint"""
    if file_type == 'pdf':
        raw_text = extract_text_from_pdf(file_path)
    elif file_type == 'docx':
        raw_text = extract_text_from_docx(file_path)
    else:
        with open(file_path, 'r') as f:
            raw_text = f.read()
    
    cleaned_text = clean_text(raw_text)
    
    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "raw_length": len(raw_text),
        "cleaned_length": len(cleaned_text),
        "improvement": f"{((len(raw_text) - len(cleaned_text)) / len(raw_text) * 100):.1f}% cleaner"
    }

def enhanced_similarity_scoring(resume_text: str, job_description: str):
    """Enhanced similarity for Arsenii's optimization endpoints"""
    score = compute_match_score(resume_text, job_description)
    
    return {
        "similarity_score": score,
        "percentage": f"{score * 100:.1f}%",
        "quality": "excellent" if score > 0.8 else "good" if score > 0.6 else "moderate" if score > 0.4 else "needs improvement",
        "model": "SentenceTransformer all-MiniLM-L6-v2"
    }