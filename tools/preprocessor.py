# tools/preprocessor.py
from tools.pdf_parser import extract_pdf_text
from tools.docx_parser import extract_docx_text
from tools.text_cleaner import clean_resume_text
from tools.match_score import calculate_match_score
import os
import time
import logging
from typing import Dict, Optional

def process_uploaded_file(file_path: str, file_type: Optional[str] = None) -> Dict:
    """
    Complete file processing pipeline for Arsenii's API integration.
    
    Args:
        file_path (str): Path to uploaded file
        file_type (str, optional): File extension override
        
    Returns:
        Dict: Processing results with metadata
    """
    start_time = time.time()
    
    try:
        # Determine file type
        if not file_type:
            file_type = os.path.splitext(file_path)[1].lower().lstrip('.')
        
        # Extract text based on file type
        if file_type == "pdf":
            raw_text = extract_pdf_text(file_path)
        elif file_type in ["docx", "doc"]:
            raw_text = extract_docx_text(file_path)
        elif file_type == "txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Clean the extracted text
        cleaned_text = clean_resume_text(raw_text)
        
        # Calculate processing metrics
        processing_time = time.time() - start_time
        
        return {
            "success": True,
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "raw_length": len(raw_text),
            "cleaned_length": len(cleaned_text),
            "processing_time": round(processing_time, 3),
            "file_type": file_type,
            "improvement_ratio": len(cleaned_text) / len(raw_text) if raw_text else 0
        }
        
    except Exception as e:
        logging.error(f"File processing error for {file_path}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "file_type": file_type,
            "processing_time": time.time() - start_time
        }

def calculate_enhanced_similarity(resume_text: str, job_description: str) -> Dict:
    """
    Enhanced similarity calculation with metadata for API responses.
    
    Args:
        resume_text (str): Resume content
        job_description (str): Job description content
        
    Returns:
        Dict: Similarity analysis with recommendations
    """
    try:
        # Calculate semantic similarity
        semantic_score = calculate_match_score(resume_text, job_description)
        
        # Basic keyword overlap for comparison
        resume_words = set(resume_text.lower().split())
        job_words = set(job_description.lower().split())
        
        if job_words:
            keyword_overlap = len(resume_words.intersection(job_words)) / len(job_words)
        else:
            keyword_overlap = 0.0
        
        # Combined weighted score
        combined_score = (semantic_score * 0.7 + keyword_overlap * 0.3)
        
        # Generate recommendation
        if combined_score >= 0.8:
            recommendation = "Excellent match - strong alignment with job requirements"
            priority = "low"
        elif combined_score >= 0.6:
            recommendation = "Good match - consider minor optimizations"
            priority = "medium"
        elif combined_score >= 0.4:
            recommendation = "Moderate match - improvements recommended"
            priority = "high"
        else:
            recommendation = "Low match - significant optimization needed"
            priority = "critical"
        
        return {
            "semantic_similarity": round(semantic_score, 4),
            "keyword_overlap": round(keyword_overlap, 4),
            "combined_score": round(combined_score, 4),
            "percentage": round(combined_score * 100, 1),
            "recommendation": recommendation,
            "priority": priority,
            "model_used": "all-MiniLM-L6-v2",
            "analysis_type": "semantic + keyword"
        }
        
    except Exception as e:
        logging.error(f"Similarity calculation error: {str(e)}")
        return {
            "semantic_similarity": 0.0,
            "keyword_overlap": 0.0,
            "combined_score": 0.0,
            "percentage": 0.0,
            "recommendation": "Analysis failed",
            "priority": "error",
            "error": str(e)
        }

# Keep your original functions for backward compatibility
def preprocess_file(file_path: str) -> str:
    """Backward compatibility wrapper"""
    result = process_uploaded_file(file_path)
    return result.get("cleaned_text", "") if result.get("success") else ""

def preprocess_text(text: str) -> str:
    """Clean raw text input (e.g. from pasted job descriptions)"""
    return clean_resume_text(text)