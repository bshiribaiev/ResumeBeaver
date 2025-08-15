import uvicorn
from fastapi import FastAPI

# load .env BEFORE importing anything that might read env vars
from dotenv import load_dotenv
# Load environment variables FIRST
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from routes import router

import logging

# Set up logging
logging.basicConfig(level=getattr(logging, __import__("os").getenv("LOG_LEVEL", "INFO")))
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Resume Optimizer API",
    description="AI-powered resume tailoring for job applications",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include unified routes
app.include_router(router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "Resume Optimizer API",
        "version": "2.0.0",
        "status": "operational",
        "docs": "/docs",
        "message": "Simplified, unified API with optional AI enhancement"
    }

@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("🦫 ResumeBeaver API starting up...")
    
    # Test Watson availability
    try:
        from watson_client import get_watson_client
        client = get_watson_client()
        if client.watson_available:
            logger.info("✅ Watson AI client available")
        else:
            logger.warning("⚠️ Watson AI client not available - using fallback mode")
    except Exception as e:
        logger.error(f"❌ Watson client error: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)