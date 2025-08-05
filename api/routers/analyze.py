from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import spacy
import re
from collections import Counter

router = APIRouter()

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

class JobDescription(BaseModel):
    content: str
    company_name: Optional[str] = None
    job_title: Optional[str] = None

class JobAnalysis(BaseModel):
    job_description: str
    required_skills: List[str]
    preferred_skills: List[str]
    key_requirements: List[str]
    experience_level: Optional[str]
    education_requirements: List[str]
    company_info: Optional[dict]
    keywords: List[str]

class ResumeText(BaseModel):
    content: str

class ResumeAnalysis(BaseModel):
    skills_found: List[str]
    experience_years: Optional[str]
    education_level: Optional[str]
    keywords: List[str]
    summary_points: List[str]

def extract_skills(text: str) -> List[str]:
    """Extract technical skills from text"""
    # Common technical skills patterns
    skill_patterns = [
        # Programming languages
        r'\b(?:Python|JavaScript|Java|C\+\+|C#|React|Vue|Angular|Node\.js|PHP|Ruby|Go|Rust|Swift|Kotlin)\b',
        # Frameworks and libraries
        r'\b(?:Django|Flask|FastAPI|Express|Spring|Laravel|Rails|TensorFlow|PyTorch|Pandas|NumPy)\b',
        # Databases
        r'\b(?:MySQL|PostgreSQL|MongoDB|Redis|SQLite|Oracle|SQL Server|DynamoDB)\b',
        # Cloud and DevOps
        r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|GitHub|GitLab|CI/CD)\b',
        # Tools and technologies
        r'\b(?:REST|API|GraphQL|JSON|XML|HTML|CSS|SASS|Linux|Windows|macOS)\b',
        # Soft skills
        r'\b(?:leadership|communication|teamwork|problem[\-\s]solving|analytical|creative)\b'
    ]
    
    skills = set()
    text_lower = text.lower()
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        skills.update(matches)
    
    # Use spaCy for additional entity extraction
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT'] and len(ent.text) > 2:
            skills.add(ent.text.lower())
    
    return sorted(list(skills))

def extract_requirements(text: str) -> List[str]:
    """Extract key requirements from job description"""
    requirements = []
    
    # Look for requirement patterns
    requirement_patterns = [
        r'(?:required|must have|essential)[\s\:]+([^\.]+)',
        r'(?:minimum|at least)\s+(\d+\+?\s+years?)\s+(?:of\s+)?experience',
        r'(?:bachelor\'?s?|master\'?s?|phd|degree)\s+(?:in\s+)?([^\.]+)',
        r'(?:experience\s+(?:with|in))\s+([^\.]+)',
    ]
    
    for pattern in requirement_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = ' '.join(match)
            requirements.append(match.strip())
    
    return requirements[:10]  # Limit to top 10

def extract_experience_level(text: str) -> Optional[str]:
    """Extract required experience level"""
    experience_patterns = [
        r'(\d+\+?)\s+years?\s+(?:of\s+)?experience',
        r'(?:entry[\-\s]level|junior|senior|lead|principal)',
        r'(?:internship|intern|graduate|mid[\-\s]level)',
    ]
    
    for pattern in experience_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    
    return None

def extract_keywords(text: str, top_n: int = 20) -> List[str]:
    """Extract most important keywords using spaCy"""
    doc = nlp(text)
    
    # Filter tokens: no stop words, punctuation, or short words
    keywords = [
        token.lemma_.lower() 
        for token in doc 
        if not token.is_stop 
        and not token.is_punct 
        and len(token.text) > 2
        and token.pos_ in ['NOUN', 'ADJ', 'VERB']
    ]
    
    # Count frequency and return top keywords
    keyword_freq = Counter(keywords)
    return [word for word, freq in keyword_freq.most_common(top_n)]

@router.post("/analyze-job", response_model=JobAnalysis)
async def analyze_job_description(job: JobDescription):
    """Analyze job description to extract requirements and skills"""
    try:
        content = job.content
        
        # Extract various components
        required_skills = extract_skills(content)
        key_requirements = extract_requirements(content)
        experience_level = extract_experience_level(content)
        keywords = extract_keywords(content)
        
        # Separate required vs preferred (basic heuristic)
        preferred_indicators = ['preferred', 'nice to have', 'bonus', 'plus']
        preferred_skills = []
        
        for skill in required_skills[:]:
            for indicator in preferred_indicators:
                if indicator in content.lower():
                    # This is a simplified approach - could be more sophisticated
                    if skill in content.lower()[content.lower().find(indicator):]:
                        preferred_skills.append(skill)
                        required_skills.remove(skill)
                        break
        
        # Extract education requirements
        education_requirements = []
        education_patterns = [
            r'(?:bachelor\'?s?|master\'?s?|phd|degree)\s+(?:in\s+)?([^\.]+)',
            r'(?:bs|ba|ms|ma|mba|phd)\s+(?:in\s+)?([^\.]+)'
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            education_requirements.extend([match.strip() for match in matches])
        
        return JobAnalysis(
            job_description=content[:500] + "..." if len(content) > 500 else content,
            required_skills=required_skills[:15],  # Limit to top 15
            preferred_skills=preferred_skills[:10],
            key_requirements=key_requirements,
            experience_level=experience_level,
            education_requirements=education_requirements[:5],
            company_info={"name": job.company_name} if job.company_name else None,
            keywords=keywords
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@router.post("/analyze-resume", response_model=ResumeAnalysis)
async def analyze_resume_text(resume: ResumeText):
    """Analyze resume text to extract skills and key information"""
    try:
        content = resume.content
        
        # Extract skills
        skills_found = extract_skills(content)
        
        # Extract experience years
        experience_years = extract_experience_level(content)
        
        # Extract education level
        education_patterns = [
            r'(?:bachelor\'?s?|master\'?s?|phd|degree)',
            r'(?:bs|ba|ms|ma|mba|phd)',
            r'(?:university|college|institute)'
        ]
        
        education_level = None
        for pattern in education_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                education_level = match.group(0).strip()
                break
        
        # Extract keywords
        keywords = extract_keywords(content)
        
        # Extract key summary points (simplified)
        sentences = content.split('.')
        summary_points = [
            sentence.strip() 
            for sentence in sentences[:5] 
            if len(sentence.strip()) > 20
        ]
        
        return ResumeAnalysis(
            skills_found=skills_found[:20],
            experience_years=experience_years,
            education_level=education_level,
            keywords=keywords,
            summary_points=summary_points
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume analysis error: {str(e)}")

@router.get("/test-analyze")
async def test_analyze_endpoint():
    """Test endpoint to verify analyze router is working"""
    return {
        "message": "Analyze router is working!",
        "endpoints": [
            "POST /analyze-job - Analyze job description",
            "POST /analyze-resume - Analyze resume text"
        ],
        "features": [
            "Skill extraction",
            "Requirement analysis", 
            "Keyword extraction",
            "Experience level detection"
        ]
    }