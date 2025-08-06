# tools/match_score.py
from sentence_transformers import SentenceTransformer, util
import logging
from functools import lru_cache

# Enhanced: Cache model loading for performance
@lru_cache(maxsize=1)
def get_similarity_model():
    """Load and cache the SentenceTransformer model"""
    return SentenceTransformer('all-MiniLM-L6-v2')

def calculate_match_score(resume_text: str, job_description: str) -> float:
    """
    Calculate semantic similarity between resume and job description.
    
    Uses SentenceTransformer all-MiniLM-L6-v2 model for semantic understanding
    that goes beyond keyword matching to understand contextual meaning.
    
    Args:
        resume_text (str): Resume content to analyze
        job_description (str): Job description to match against
        
    Returns:
        float: Similarity score between 0.0 and 1.0
               0.0 = No similarity, 1.0 = Perfect match
               
    Example:
        >>> score = calculate_match_score(
        ...     "Python developer with Django experience",
        ...     "Looking for Python programmer with web framework knowledge"
        ... )
        >>> print(f"Match score: {score:.3f}")
    """
    try:
        if not resume_text or not job_description:
            return 0.0
        
        model = get_similarity_model()
        
        # Enhanced: Preprocess text for better embedding
        resume_clean = resume_text.strip()[:500]  # Limit length for better performance
        job_clean = job_description.strip()[:500]
        
        # Calculate embeddings
        resume_embedding = model.encode(resume_clean, convert_to_tensor=True)
        job_embedding = model.encode(job_clean, convert_to_tensor=True)
        
        # Calculate cosine similarity
        similarity = util.cos_sim(resume_embedding, job_embedding)
        score = float(similarity.item())
        
        # Enhanced: Log calculation for debugging
        logging.info(f"Match score calculated: {score:.4f}")
        
        return round(score, 4)
        
    except Exception as e:
        logging.error(f"Match score calculation error: {str(e)}")
        return 0.0

# Keep your original function name for backward compatibility
def compute_match_score(resume_text: str, job_text: str) -> float:
    """Backward compatibility wrapper"""
    return calculate_match_score(resume_text, job_text)