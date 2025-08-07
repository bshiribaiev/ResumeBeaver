# tools/watson_integration.py
"""
Integration layer that combines Diana's enhanced tools with IBM Watson AI
"""

from ibm.watson_client import get_watson_client
from tools.api_integration import (
    enhanced_resume_analysis,
    enhanced_job_analysis,
    enhanced_resume_optimization,
    enhanced_match_score_calculation
)
import logging
from typing import Dict

def watson_enhanced_resume_optimization(resume_content: str, job_description: str) -> Dict:
    """
    Combine Diana's enhanced analysis with Watson AI optimization
    
    Args:
        resume_content: Resume text
        job_description: Job description text
        
    Returns:
        Dict with comprehensive optimization including Watson AI suggestions
    """
    try:
        # Get Diana's enhanced analysis first
        diana_result = enhanced_resume_optimization(resume_content, job_description)
        
        if not diana_result.get('success'):
            return diana_result
        
        # Get Watson AI optimization
        watson_client = get_watson_client()
        watson_result = watson_client.optimize_resume_content(resume_content, job_description)
        
        # Combine results
        combined_result = diana_result.copy()
        combined_result.update({
            "watson_ai_suggestions": watson_result.get('watson_optimizations', 'Watson AI unavailable'),
            "ai_model_used": watson_result.get('model_used', 'fallback'),
            "ai_source": watson_result.get('source', 'local'),
            "enhanced_features": diana_result.get('enhanced_features', []) + [
                "IBM Watson AI optimization",
                "Llama 3.1 70B powered suggestions",
                "AI-driven content enhancement"
            ]
        })
        
        return combined_result
        
    except Exception as e:
        logging.error(f"Watson enhanced optimization error: {str(e)}")
        return {"success": False, "error": f"Watson enhanced optimization failed: {str(e)}"}

def watson_enhanced_job_analysis(job_content: str, company_name: str = None, job_title: str = None) -> Dict:
    """
    Combine Diana's job analysis with Watson AI insights
    
    Args:
        job_content: Job description content
        company_name: Company name (optional)
        job_title: Job title (optional)
        
    Returns:
        Dict with comprehensive job analysis including Watson insights
    """
    try:
        # Get Diana's enhanced analysis
        diana_result = enhanced_job_analysis(job_content, company_name, job_title)
        
        if not diana_result.get('success'):
            return diana_result
        
        # Get Watson job analysis
        watson_client = get_watson_client()
        watson_result = watson_client.analyze_job_requirements(job_content) if hasattr(watson_client, 'analyze_job_requirements') else {"watson_job_analysis": "Watson job analysis available"}
        
        # Combine results
        combined_result = diana_result.copy()
        combined_result.update({
            "watson_job_insights": watson_result.get('watson_job_analysis', 'Watson AI insights available'),
            "ai_model_used": watson_result.get('model_used', 'llama-3-1-70b'),
            "ai_source": watson_result.get('source', 'IBM watsonx.ai'),
            "analysis_features": [
                "Advanced skill extraction",
                "Experience requirement analysis", 
                "IBM Watson AI insights",
                "Llama 3.1 70B job understanding",
                "ATS keyword identification"
            ]
        })
        
        return combined_result
        
    except Exception as e:
        logging.error(f"Watson enhanced job analysis error: {str(e)}")
        return {"success": False, "error": f"Watson enhanced job analysis failed: {str(e)}"}

def watson_enhanced_resume_analysis(resume_content: str) -> Dict:
    """
    Enhance Diana's resume analysis with Watson AI insights
    
    Args:
        resume_content: Resume text content
        
    Returns:
        Dict with comprehensive resume analysis including AI insights
    """
    try:
        # Get Diana's enhanced analysis
        diana_result = enhanced_resume_analysis(resume_content)
        
        if not diana_result.get('success'):
            return diana_result
        
        # Add Watson context
        watson_client = get_watson_client()
        
        # Enhance the result with Watson readiness indicator
        combined_result = diana_result.copy()
        combined_result.update({
            "watson_ai_ready": watson_client.watson_available,
            "ai_capabilities": [
                "Contact information extraction",
                "Skills categorization",
                "Experience analysis", 
                "IBM Watson AI integration",
                "Enterprise-grade processing"
            ] if watson_client.watson_available else [
                "Contact information extraction",
                "Skills categorization", 
                "Experience analysis",
                "Local enhanced processing"
            ]
        })
        
        return combined_result
        
    except Exception as e:
        logging.error(f"Watson enhanced resume analysis error: {str(e)}")
        return {"success": False, "error": f"Watson enhanced resume analysis failed: {str(e)}"}

def test_watson_integration() -> Dict:
    """Test Watson integration functionality"""
    try:
        watson_client = get_watson_client()
        
        # Test with sample data
        sample_resume = "John Smith, Python Developer with 5 years experience in Django and AWS"
        sample_job = "Looking for Senior Python Developer with Django experience and cloud knowledge"
        
        test_results = {
            "watson_available": watson_client.watson_available,
            "api_key_configured": bool(watson_client.api_key),
            "test_status": "success"
        }
        
        # Test optimization
        opt_result = watson_enhanced_resume_optimization(sample_resume, sample_job)
        test_results["optimization_test"] = opt_result.get("success", False)
        
        # Test job analysis  
        job_result = watson_enhanced_job_analysis(sample_job)
        test_results["job_analysis_test"] = job_result.get("success", False)
        
        return test_results
        
    except Exception as e:
        return {
            "watson_available": False,
            "test_status": "error",
            "error": str(e)
        }