import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)