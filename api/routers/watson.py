# api/routers/watson.py
"""
IBM Watson-powered endpoints for ResumeBeaver
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from tools.watson_integration import (
    watson_enhanced_resume_optimization,
    watson_enhanced_job_analysis,
    watson_enhanced_resume_analysis,
    test_watson_integration
)

router = APIRouter()

class WatsonOptimizationRequest(BaseModel):
    resume_content: str
    job_description: str
    job_title: Optional[str] = None
    company_name: Optional[str] = None

class WatsonJobAnalysisRequest(BaseModel):
    content: str
    company_name: Optional[str] = None
    job_title: Optional[str] = None

class WatsonResumeAnalysisRequest(BaseModel):
    content: str

@router.post("/watson-optimize-resume")
async def watson_optimize_resume(request: WatsonOptimizationRequest):
    """
    Ultimate resume optimization using IBM Watson AI + Diana's enhanced tools
    
    This endpoint combines:
    - Diana's semantic analysis and skill extraction
    - IBM watsonx.ai Llama 3.1 70B optimization suggestions
    - Advanced ATS scoring and recommendations
    """
    try:
        result = watson_enhanced_resume_optimization(
            request.resume_content, 
            request.job_description
        )
        
        if result.get("success"):
            return result
        raise HTTPException(status_code=500, detail=result.get("error", "Watson optimization failed"))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Watson optimization error: {str(e)}")

@router.post("/watson-analyze-job")
async def watson_analyze_job(request: WatsonJobAnalysisRequest):
    """
    Advanced job analysis using IBM Watson AI + enhanced processing
    
    Features:
    - AI-powered requirement extraction using Llama 3.1 70B
    - Advanced skill categorization
    - Experience level analysis
    - ATS keyword identification
    """
    try:
        result = watson_enhanced_job_analysis(
            request.content,
            request.company_name,
            request.job_title
        )
        
        if result.get("success"):
            return result
        raise HTTPException(status_code=500, detail=result.get("error", "Watson job analysis failed"))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Watson job analysis error: {str(e)}")

@router.post("/watson-analyze-resume")
async def watson_analyze_resume(request: WatsonResumeAnalysisRequest):
    """
    Comprehensive resume analysis with Watson AI readiness
    
    Features:
    - Contact information extraction
    - Skills categorization by technology type
    - Experience level assessment
    - Watson AI integration status
    """
    try:
        result = watson_enhanced_resume_analysis(request.content)
        
        if result.get("success"):
            return result
        raise HTTPException(status_code=500, detail=result.get("error", "Watson resume analysis failed"))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Watson resume analysis error: {str(e)}")

@router.get("/watson-status")
async def watson_status():
    """
    Check IBM Watson integration status and capabilities
    """
    try:
        status = test_watson_integration()
        return {
            "watson_integration": "active",
            "watson_available": status.get("watson_available", False),
            "api_configured": status.get("api_key_configured", False),
            "model": "meta-llama/llama-3-1-70b-instruct",
            "capabilities": [
                "AI-powered resume optimization",
                "Intelligent job requirement extraction",
                "Advanced content enhancement",
                "Semantic similarity matching",
                "ATS optimization scoring"
            ],
            "endpoints": [
                "POST /watson-optimize-resume - Ultimate AI optimization",
                "POST /watson-analyze-job - AI job analysis",
                "POST /watson-analyze-resume - Enhanced resume analysis"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Watson status check failed: {str(e)}")

@router.get("/test-watson")
async def test_watson_endpoint():
    """Test Watson integration with sample data"""
    try:
        # Test with sample data
        sample_resume = """
        Jane Doe
        Senior Software Engineer
        jane.doe@email.com | (555) 987-6543
        
        EXPERIENCE
        Senior Developer at TechCorp (2019-Present)
        - Led development of microservices using Python and AWS
        - Built React frontends serving 50K+ users
        - Implemented CI/CD pipelines with Jenkins
        
        SKILLS
        Python, JavaScript, React, AWS, Docker, PostgreSQL
        """
        
        sample_job = """
        Senior Python Developer Position
        
        We're seeking a Senior Python Developer with:
        - 5+ years Python development experience
        - AWS cloud platform expertise
        - React/JavaScript frontend skills
        - Docker containerization experience
        - Bachelor's degree in Computer Science
        """
        
        # Test Watson optimization
        result = watson_enhanced_resume_optimization(sample_resume, sample_job)
        
        return {
            "test_status": "success" if result.get("success") else "failed",
            "watson_available": result.get("ai_source") == "IBM watsonx.ai",
            "sample_optimization": result.get("watson_ai_suggestions", "No suggestions available")[:200] + "...",
            "model_used": result.get("ai_model_used", "unknown"),
            "message": "Watson integration test completed successfully!"
        }
        
    except Exception as e:
        return {
            "test_status": "error",
            "error": str(e),
            "message": "Watson integration test failed"
        }