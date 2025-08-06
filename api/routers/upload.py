# api/routers/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from datetime import datetime
import PyPDF2
from docx import Document

router = APIRouter()

# Configure upload settings
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".doc"]

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    text = ""
    try:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading DOCX: {str(e)}")

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and process a resume file (PDF or DOCX)"""
    
    # Validate file type
    if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported. Allowed: {ALLOWED_EXTENSIONS}"
        )
    
    # Validate file size
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
        )
    
    try:
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        upload_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text from file
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension == '.pdf':
            extracted_text = extract_text_from_pdf(upload_path)
        elif file_extension in ['.docx', '.doc']:
            extracted_text = extract_text_from_docx(upload_path)
        else:
            raise Exception("Unsupported file type")
        
        return {
            "message": "Resume uploaded successfully",
            "filename": file.filename,
            "saved_as": safe_filename,
            "size": file.size,
            "text_length": len(extracted_text),
            "preview": extracted_text[:300] + "..." if len(extracted_text) > 300 else extracted_text,
            "upload_timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        # Clean up file if processing failed
        if 'upload_path' in locals() and os.path.exists(upload_path):
            os.remove(upload_path)
        raise HTTPException(status_code=500, detail=f"File processing error: {str(e)}")

@router.get("/files")
async def list_uploaded_files():
    """List all uploaded resume files"""
    try:
        files = []
        for filename in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                files.append({
                    "filename": filename,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        return {"files": files, "total": len(files)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

@router.get("/test-upload")
async def test_upload_endpoint():
    """Test endpoint to verify upload router is working"""
    return {
        "message": "Upload router is working!",
        "endpoints": [
            "POST /upload-resume - Upload resume file",
            "GET /files - List uploaded files"
        ],
        "supported_formats": ALLOWED_EXTENSIONS,
        "max_file_size": f"{MAX_FILE_SIZE / (1024*1024):.1f}MB"
    }