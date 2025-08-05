from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routers import upload, analyze  # ← Updated this line

# Create FastAPI app
app = FastAPI(
    title="Resume Builder API",
    description="AI-powered resume tailoring backend",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoints
@app.get("/")
async def root():
    return {"message": "Resume Builder API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Resume Builder Backend"}

@app.get("/test-imports")
async def test_imports():
    try:
        import spacy
        import pandas
        import numpy
        nlp = spacy.load('en_core_web_sm')
        
        return {
            "status": "success",
            "imports": {
                "spacy": "✅",
                "pandas": "✅", 
                "numpy": "✅",
                "spacy_model": "✅"
            },
            "message": "All imports working correctly!"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

# Include routers
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(analyze.router, prefix="/api/v1", tags=["analyze"])  # ← Added this line

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)