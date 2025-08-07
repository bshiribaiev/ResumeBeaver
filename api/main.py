# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routers import upload, analyze, optimize, watson  # ← Added watson

# Create FastAPI app
app = FastAPI(
    title="Resume Builder API",
    description="AI-powered resume tailoring backend with IBM Watson integration",
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
    return {"message": "Resume Builder API with IBM Watson AI is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Resume Builder Backend with Watson AI"}

@app.get("/test-imports")
async def test_imports():
    try:
        import spacy
        import pandas
        import numpy
        import sklearn
        import requests  # ← Added for Watson
        from ibm.watson_client import get_watson_client  # ← Added Watson test
        nlp = spacy.load('en_core_web_sm')
        
        # Test Watson client
        watson_client = get_watson_client()
        
        return {
            "status": "success",
            "imports": {
                "spacy": "✅",
                "pandas": "✅", 
                "numpy": "✅",
                "sklearn": "✅",
                "requests": "✅",
                "watson_client": "✅",
                "spacy_model": "✅"
            },
            "watson_status": {
                "watson_available": watson_client.watson_available,
                "api_configured": bool(watson_client.api_key)
            },
            "message": "All imports working correctly with Watson integration!"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

# Include routers
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(analyze.router, prefix="/api/v1", tags=["analyze"])
app.include_router(optimize.router, prefix="/api/v1", tags=["optimize"])
app.include_router(watson.router, prefix="/api/v1", tags=["watson"])  # ← Added Watson router

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)