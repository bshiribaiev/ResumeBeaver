import re
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil
from datetime import datetime
import PyPDF2
from docx import Document
from resume_processor import ResumeAnalyzer

router = APIRouter()

# Initialize analyzer (Watson will auto-detect availability)
analyzer = ResumeAnalyzer(use_watson=True)

# Request/Response models
class AnalyzeRequest(BaseModel):
    content: str
    type: str = "resume"  # "resume" or "job"
class OptimizeRequest(BaseModel):
    resume: str
    job_description: str
class MatchRequest(BaseModel):
    resume: str
    job_description: str

# Extract text from uploaded file
def extract_file_text(file_path: str, file_type: str) -> str:
    try:
        if file_type == 'pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        elif file_type in ['docx', 'doc']:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs if para.text])
            
            # Also extract from tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = " | ".join([cell.text for cell in row.cells if cell.text])
                    if row_text:
                        text += "\n" + row_text
            return text.strip()
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        raise Exception(f"Failed to extract text: {str(e)}")

# Upload and process resume file
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(400, f"File type not supported. Allowed: {allowed_extensions}")
    if file.size > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(400, "File too large (max 10MB)")
    try:
        # Save file temporarily
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{timestamp}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # Extract and analyze text
        text = extract_file_text(file_path, file_ext[1:])
        analysis = analyzer.analyze_resume(text)
        return {
            "success": True,
            "filename": file.filename,
            "file_size": file.size,
            "text_preview": text[:500] + "..." if len(text) > 500 else text,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        # Clean up on error
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(500, f"Processing failed: {str(e)}")

# Analyze resume or job description
@router.post("/analyze")
async def analyze_content(request: AnalyzeRequest):
    try:
        if request.type == "resume":
            result = analyzer.analyze_resume(request.content)
        else:  # job description
            skills = analyzer.extract_skills(request.content)
            # Extract requirements
            exp_matches = re.findall(r'(\d+)\+?\s*years?', request.content, re.IGNORECASE)
            years_required = max(map(int, exp_matches)) if exp_matches else None
            result = {
                "skills_required": skills,
                "years_experience": years_required,
                "word_count": len(request.content.split()),
                "type": "job_description"
            }
        return {
            "success": True,
            "analysis": result,
            "ai_powered": result.get('ai_powered', False)
        }
    except Exception as e:
        raise HTTPException(500, f"Analysis failed: {str(e)}")

# Calculate match score between resume and job
@router.post("/match")
async def calculate_match(request: MatchRequest):
    try:
        result = analyzer.calculate_match_score(
            request.resume,
            request.job_description
        )
        return {
            "success": True,
            "match_analysis": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(500, f"Match calculation failed: {str(e)}")

# Optimize resume for specific job
@router.post("/optimize")
async def optimize_resume(request: OptimizeRequest):
    try:
        result = analyzer.optimize_resume(
            request.resume,
            request.job_description
        )
        return {
            "success": True,
            "optimization": result,
            "ai_powered": result.get('ai_powered', False),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(500, f"Optimization failed: {str(e)}")

# Check system status
@router.get("/status")
async def get_status():
    watson_available = False
    try:
        from watson_client import get_watson_client
        client = get_watson_client()
        watson_available = client.watson_available
    except:
        pass
    return {
        "status": "operational",
        "version": "2.0.0",
        "features": {
            "file_upload": True,
            "resume_analysis": True,
            "job_analysis": True,
            "match_scoring": True,
            "optimization": True,
            "ai_powered": watson_available
        },
        "ai_status": {
            "watson_available": watson_available,
            "model": "meta-llama/llama-3-1-70b-instruct" if watson_available else None
        },
        "endpoints": [
            "POST /upload - Upload and process resume file",
            "POST /analyze - Analyze resume or job content",
            "POST /match - Calculate resume-job match score",
            "POST /optimize - Generate optimization suggestions",
            "GET /status - System status and capabilities"
        ]
    }

# Health check
@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Resume Optimizer API"}