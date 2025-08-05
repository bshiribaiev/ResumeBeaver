from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import re
from collections import Counter
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

router = APIRouter()

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

class OptimizationRequest(BaseModel):
    resume_content: str
    job_description: str
    job_title: Optional[str] = None
    company_name: Optional[str] = None

class MatchScore(BaseModel):
    overall_score: float
    skill_match_score: float
    keyword_match_score: float
    experience_match_score: float
    education_match_score: float

class Improvement(BaseModel):
    category: str
    suggestion: str
    priority: str  # "high", "medium", "low"
    impact_score: float

class OptimizationResult(BaseModel):
    match_score: MatchScore
    missing_skills: List[str]
    suggested_keywords: List[str]
    improvements: List[Improvement]
    optimized_sections: Dict[str, str]
    ats_score: float
    ats_recommendations: List[str]

def extract_skills(text: str) -> List[str]:
    """Extract technical skills from text"""
    skill_patterns = [
        # Programming languages
        r'\b(?:Python|JavaScript|Java|C\+\+|C#|React|Vue|Angular|Node\.js|PHP|Ruby|Go|Rust|Swift|Kotlin|TypeScript)\b',
        # Frameworks and libraries
        r'\b(?:Django|Flask|FastAPI|Express|Spring|Laravel|Rails|TensorFlow|PyTorch|Pandas|NumPy|jQuery|Bootstrap)\b',
        # Databases
        r'\b(?:MySQL|PostgreSQL|MongoDB|Redis|SQLite|Oracle|SQL Server|DynamoDB|Cassandra)\b',
        # Cloud and DevOps
        r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|GitHub|GitLab|CI/CD|Terraform|Ansible)\b',
        # Tools and technologies
        r'\b(?:REST|API|GraphQL|JSON|XML|HTML|CSS|SASS|Linux|Windows|macOS|Figma|Sketch)\b',
        # Data Science/ML
        r'\b(?:Machine Learning|ML|AI|Data Science|Analytics|Tableau|Power BI|Excel|R|Stata)\b'
    ]
    
    skills = set()
    text_lower = text.lower()
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        skills.update(match.lower() for match in matches)
    
    return list(skills)

def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate cosine similarity between two texts using TF-IDF"""
    try:
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except:
        return 0.0

def extract_experience_years(text: str) -> Optional[int]:
    """Extract years of experience from text"""
    patterns = [
        r'(\d+)\+?\s+years?\s+(?:of\s+)?experience',
        r'(\d+)\+?\s+years?\s+(?:in|with)',
        r'experience.*?(\d+)\+?\s+years?'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None

def calculate_match_score(resume: str, job_desc: str) -> MatchScore:
    """Calculate comprehensive match score between resume and job description"""
    
    # Extract skills from both
    resume_skills = set(extract_skills(resume))
    job_skills = set(extract_skills(job_desc))
    
    # Skill match score
    if job_skills:
        skill_match = len(resume_skills.intersection(job_skills)) / len(job_skills)
    else:
        skill_match = 0.0
    
    # Keyword similarity using TF-IDF
    keyword_match = calculate_text_similarity(resume, job_desc)
    
    # Experience match
    resume_exp = extract_experience_years(resume)
    job_exp = extract_experience_years(job_desc)
    
    if resume_exp and job_exp:
        if resume_exp >= job_exp:
            experience_match = 1.0
        else:
            experience_match = resume_exp / job_exp
    else:
        experience_match = 0.5  # Neutral when can't determine
    
    # Education match (simplified)
    education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
    resume_education = sum(1 for keyword in education_keywords if keyword in resume.lower())
    job_education = sum(1 for keyword in education_keywords if keyword in job_desc.lower())
    
    if job_education > 0:
        education_match = min(resume_education / job_education, 1.0)
    else:
        education_match = 1.0
    
    # Overall weighted score
    weights = {'skill': 0.4, 'keyword': 0.3, 'experience': 0.2, 'education': 0.1}
    overall = (
        skill_match * weights['skill'] +
        keyword_match * weights['keyword'] +
        experience_match * weights['experience'] +
        education_match * weights['education']
    )
    
    return MatchScore(
        overall_score=round(overall * 100, 1),
        skill_match_score=round(skill_match * 100, 1),
        keyword_match_score=round(keyword_match * 100, 1),
        experience_match_score=round(experience_match * 100, 1),
        education_match_score=round(education_match * 100, 1)
    )

def identify_missing_skills(resume: str, job_desc: str) -> List[str]:
    """Identify skills mentioned in job description but missing from resume"""
    resume_skills = set(extract_skills(resume))
    job_skills = set(extract_skills(job_desc))
    
    missing = job_skills - resume_skills
    return sorted(list(missing))

def suggest_keywords(resume: str, job_desc: str, top_n: int = 15) -> List[str]:
    """Suggest important keywords from job description to include in resume"""
    
    # Use spaCy to extract important terms from job description
    doc = nlp(job_desc)
    
    # Extract meaningful keywords
    keywords = []
    for token in doc:
        if (not token.is_stop and 
            not token.is_punct and 
            len(token.text) > 2 and
            token.pos_ in ['NOUN', 'ADJ', 'VERB'] and
            token.text.lower() not in resume.lower()):
            keywords.append(token.lemma_.lower())
    
    # Count frequency and return top keywords
    keyword_freq = Counter(keywords)
    return [word for word, freq in keyword_freq.most_common(top_n)]

def generate_improvements(resume: str, job_desc: str, match_score: MatchScore) -> List[Improvement]:
    """Generate specific improvement suggestions"""
    improvements = []
    
    # Skill-based improvements
    if match_score.skill_match_score < 70:
        missing_skills = identify_missing_skills(resume, job_desc)
        if missing_skills:
            improvements.append(Improvement(
                category="Skills",
                suggestion=f"Add these relevant skills: {', '.join(missing_skills[:5])}",
                priority="high",
                impact_score=8.5
            ))
    
    # Keyword improvements
    if match_score.keyword_match_score < 60:
        improvements.append(Improvement(
            category="Keywords",
            suggestion="Incorporate more job-specific terminology and keywords throughout your resume",
            priority="high",
            impact_score=7.0
        ))
    
    # Experience improvements
    if match_score.experience_match_score < 80:
        improvements.append(Improvement(
            category="Experience",
            suggestion="Highlight relevant experience more prominently and quantify achievements",
            priority="medium",
            impact_score=6.5
        ))
    
    # ATS improvements
    improvements.append(Improvement(
        category="ATS Optimization",
        suggestion="Use standard section headings and avoid complex formatting",
        priority="medium",
        impact_score=5.0
    ))
    
    return improvements

def calculate_ats_score(resume: str) -> tuple[float, List[str]]:
    """Calculate ATS-friendliness score and provide recommendations"""
    score = 100.0
    recommendations = []
    
    # Check for standard section headers
    standard_headers = ['experience', 'education', 'skills', 'summary', 'objective']
    found_headers = sum(1 for header in standard_headers if header in resume.lower())
    
    if found_headers < 3:
        score -= 20
        recommendations.append("Use standard section headers like 'Experience', 'Education', 'Skills'")
    
    # Check for contact information
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    
    if not re.search(email_pattern, resume):
        score -= 15
        recommendations.append("Include a professional email address")
    
    if not re.search(phone_pattern, resume):
        score -= 10
        recommendations.append("Include a phone number")
    
    # Check for special characters that might cause issues
    problematic_chars = ['•', '→', '★', '◆']
    if any(char in resume for char in problematic_chars):
        score -= 5
        recommendations.append("Replace special characters with standard punctuation")
    
    return max(score, 0), recommendations

def optimize_sections(resume: str, job_desc: str) -> Dict[str, str]:
    """Generate optimized versions of key resume sections"""
    
    # Extract key terms from job description
    doc = nlp(job_desc)
    key_terms = [token.lemma_.lower() for token in doc 
                if not token.is_stop and not token.is_punct and len(token.text) > 2]
    
    # This is a simplified version - in a real implementation, 
    # you'd use more sophisticated NLP or AI to rewrite sections
    
    suggestions = {
        "summary": "Consider incorporating these key terms in your professional summary: " + 
                  ", ".join(set(key_terms[:10])),
        "skills": "Reorganize skills section to highlight: " + 
                 ", ".join(identify_missing_skills(resume, job_desc)[:8]),
        "experience": "Quantify achievements and use action verbs that align with job requirements"
    }
    
    return suggestions

@router.post("/optimize-resume", response_model=OptimizationResult)
async def optimize_resume(request: OptimizationRequest):
    """Main optimization endpoint - analyzes resume against job description"""
    try:
        resume = request.resume_content
        job_desc = request.job_description
        
        # Calculate match score
        match_score = calculate_match_score(resume, job_desc)
        
        # Identify missing skills
        missing_skills = identify_missing_skills(resume, job_desc)
        
        # Suggest keywords
        suggested_keywords = suggest_keywords(resume, job_desc)
        
        # Generate improvement suggestions
        improvements = generate_improvements(resume, job_desc, match_score)
        
        # Optimize sections
        optimized_sections = optimize_sections(resume, job_desc)
        
        # Calculate ATS score
        ats_score, ats_recommendations = calculate_ats_score(resume)
        
        return OptimizationResult(
            match_score=match_score,
            missing_skills=missing_skills[:10],  # Limit to top 10
            suggested_keywords=suggested_keywords,
            improvements=improvements,
            optimized_sections=optimized_sections,
            ats_score=ats_score,
            ats_recommendations=ats_recommendations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization error: {str(e)}")

@router.post("/calculate-match-score")
async def calculate_job_match_score(request: OptimizationRequest):
    """Calculate just the match score between resume and job description"""
    try:
        match_score = calculate_match_score(request.resume_content, request.job_description)
        return {"match_score": match_score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Match score calculation error: {str(e)}")

@router.post("/suggest-keywords")
async def get_keyword_suggestions(request: OptimizationRequest):
    """Get keyword suggestions for ATS optimization"""
    try:
        keywords = suggest_keywords(request.resume_content, request.job_description, top_n=20)
        missing_skills = identify_missing_skills(request.resume_content, request.job_description)
        
        return {
            "suggested_keywords": keywords,
            "missing_skills": missing_skills,
            "recommendation": "Incorporate these keywords naturally throughout your resume"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Keyword suggestion error: {str(e)}")

@router.get("/test-optimize")
async def test_optimization_endpoint():
    """Test endpoint to verify optimization router is working"""
    return {
        "message": "Optimization router is working!",
        "endpoints": [
            "POST /optimize-resume - Complete resume optimization",
            "POST /calculate-match-score - Job match scoring",
            "POST /suggest-keywords - ATS keyword suggestions"
        ],
        "features": [
            "Resume-job matching analysis",
            "Missing skill identification",
            "ATS optimization scoring",
            "Improvement recommendations",
            "Keyword suggestion engine"
        ]
    }