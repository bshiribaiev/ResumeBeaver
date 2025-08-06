# tools/api_integration.py
"""
Integration bridge between Diana's enhanced tools and Arsenii's FastAPI endpoints.
This file provides enhanced functions that Arsenii can import into his routers.
"""

import sys
import os
from typing import Dict, List, Optional

# Add tools directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import Diana's enhanced tools
try:
    from tools.preprocessor import process_uploaded_file, calculate_enhanced_similarity
    from tools.resume_info_extractor import extract_comprehensive_resume_info
    from tools.match_score import calculate_match_score
    from tools.text_cleaner import clean_resume_text
    DIANA_TOOLS_AVAILABLE = True
    print("✅ Diana's enhanced tools loaded successfully!")
except ImportError as e:
    print(f"⚠️ Could not import Diana's tools: {e}")
    DIANA_TOOLS_AVAILABLE = False

def enhanced_upload_processing(file_path: str, filename: str) -> Dict:
    """
    Enhanced file processing for Arsenii's upload endpoint.
    Uses Diana's comprehensive analysis instead of basic text extraction.
    
    Args:
        file_path (str): Path to uploaded file
        filename (str): Original filename
        
    Returns:
        Dict: Enhanced processing results with comprehensive analysis
    """
    if DIANA_TOOLS_AVAILABLE:
        try:
            # Use Diana's enhanced processing
            file_type = filename.split('.')[-1].lower()
            result = process_uploaded_file(file_path, file_type)
            
            if result.get('success'):
                # Add comprehensive resume analysis
                comprehensive_info = extract_comprehensive_resume_info(result['cleaned_text'])
                
                return {
                    "success": True,
                    "message": "Resume processed with enhanced analysis",
                    "filename": filename,
                    "file_analysis": {
                        "processing_time": result['processing_time'],
                        "raw_length": result['raw_length'],
                        "cleaned_length": result['cleaned_length'],
                        "file_type": result['file_type']
                    },
                    "contact_info": comprehensive_info['contact_info'],
                    "skills_analysis": {
                        "programming_languages": comprehensive_info['skills']['programming_languages'],
                        "frameworks": comprehensive_info['skills']['frameworks_libraries'],
                        "databases": comprehensive_info['skills']['databases'], 
                        "cloud_platforms": comprehensive_info['skills']['cloud_platforms'],
                        "total_technical_skills": len(comprehensive_info['skills']['all_technical'])
                    },
                    "experience_analysis": {
                        "years_experience": comprehensive_info['years_experience']
                    },
                    "enhanced_features": [
                        "Contact information extraction",
                        "Skills categorization", 
                        "Experience analysis",
                        "Comprehensive resume parsing"
                    ]
                }
            else:
                return {
                    "success": False,
                    "error": result.get('error', 'Processing failed')
                }
                
        except Exception as e:
            return {"success": False, "error": f"Enhanced processing failed: {str(e)}"}
    
    return {
        "success": False,
        "error": "Enhanced tools not available"
    }

def enhanced_resume_analysis(resume_text: str) -> Dict:
    """
    Enhanced resume analysis for Arsenii's analyze endpoint.
    Uses Diana's comprehensive extraction instead of basic regex patterns.
    
    Args:
        resume_text (str): Resume content
        
    Returns:
        Dict: Comprehensive resume analysis
    """
    if DIANA_TOOLS_AVAILABLE:
        try:
            # Clean the text first
            cleaned_text = clean_resume_text(resume_text)
            
            # Extract comprehensive information
            analysis = extract_comprehensive_resume_info(cleaned_text)
            
            return {
                "success": True,
                "skills_found": analysis['skills']['all_technical'],
                "programming_languages": analysis['skills']['programming_languages'],
                "frameworks": analysis['skills']['frameworks_libraries'],
                "databases": analysis['skills']['databases'],
                "cloud_platforms": analysis['skills']['cloud_platforms'],
                "experience_years": ', '.join(analysis['years_experience']) if analysis['years_experience'] else None,
                "contact_info": analysis['contact_info'],
                "keywords": analysis['skills']['all_technical'][:20],
                "summary_points": [
                    f"Found {len(analysis['skills']['all_technical'])} technical skills",
                    f"Contact information: {'Complete' if analysis['contact_info']['email'] else 'Partial'}",
                    f"Experience mentioned: {', '.join(analysis['years_experience'])} years" if analysis['years_experience'] else "Experience level not specified"
                ]
            }
            
        except Exception as e:
            return {"success": False, "error": f"Enhanced analysis failed: {str(e)}"}
    
    return {"success": False, "error": "Enhanced tools not available"}

def enhanced_job_analysis(job_content: str, company_name: str = None, job_title: str = None) -> Dict:
    """
    Enhanced job analysis for Arsenii's analyze endpoint.
    
    Args:
        job_content (str): Job description content
        company_name (str, optional): Company name
        job_title (str, optional): Job title
        
    Returns:
        Dict: Enhanced job analysis
    """
    if DIANA_TOOLS_AVAILABLE:
        try:
            # Clean the job description
            cleaned_job = clean_resume_text(job_content)
            
            # Extract skills from job description using Diana's extractor
            job_skills_analysis = extract_comprehensive_resume_info(cleaned_job)
            
            return {
                "success": True,
                "job_description": job_content[:500] + "..." if len(job_content) > 500 else job_content,
                "required_skills": job_skills_analysis['skills']['all_technical'],
                "programming_languages": job_skills_analysis['skills']['programming_languages'],
                "frameworks": job_skills_analysis['skills']['frameworks_libraries'],
                "databases": job_skills_analysis['skills']['databases'],
                "cloud_platforms": job_skills_analysis['skills']['cloud_platforms'],
                "experience_requirements": job_skills_analysis['years_experience'],
                "company_info": {"name": company_name} if company_name else None,
                "job_title": job_title,
                "keywords": job_skills_analysis['skills']['all_technical'][:20]
            }
            
        except Exception as e:
            return {"success": False, "error": f"Enhanced job analysis failed: {str(e)}"}
    
    return {"success": False, "error": "Enhanced tools not available"}

def enhanced_resume_optimization(resume_content: str, job_description: str) -> Dict:
    """
    Enhanced resume optimization for Arsenii's optimize endpoint.
    Uses Diana's comprehensive matching and analysis.
    
    Args:
        resume_content (str): Resume text
        job_description (str): Job description
        
    Returns:
        Dict: Comprehensive optimization analysis
    """
    if DIANA_TOOLS_AVAILABLE:
        try:
            # Use Diana's enhanced similarity calculation
            similarity_result = calculate_enhanced_similarity(resume_content, job_description)
            
            # Extract skills from both resume and job
            resume_analysis = extract_comprehensive_resume_info(resume_content)
            job_analysis = extract_comprehensive_resume_info(job_description)
            
            # Find missing skills
            resume_skills = set(resume_analysis['skills']['all_technical'])
            job_skills = set(job_analysis['skills']['all_technical'])
            missing_skills = list(job_skills - resume_skills)
            matching_skills = list(job_skills & resume_skills)
            
            return {
                "success": True,
                "match_score": {
                    "overall_score": similarity_result['percentage'],
                    "semantic_similarity": similarity_result['semantic_similarity'] * 100,
                    "keyword_overlap": similarity_result['keyword_overlap'] * 100,
                    "recommendation": similarity_result['recommendation']
                },
                "missing_skills": missing_skills[:10],
                "matching_skills": matching_skills,
                "suggested_keywords": job_analysis['skills']['all_technical'][:15],
                "improvements": [
                    {
                        "category": "Skills",
                        "suggestion": f"Consider adding these skills: {', '.join(missing_skills[:3])}",
                        "priority": "high" if similarity_result['priority'] in ['critical', 'high'] else "medium",
                        "impact_score": 8.5
                    }
                ] if missing_skills else [],
                "ats_score": 85.0,  # Could be enhanced further
                "ats_recommendations": [
                    "Use standard section headers",
                    "Include more job-specific keywords",
                    "Quantify achievements with metrics"
                ]
            }
                
        except Exception as e:
            return {"success": False, "error": f"Enhanced optimization failed: {str(e)}"}
    
    return {"success": False, "error": "Enhanced tools not available"}

def enhanced_match_score_calculation(resume_content: str, job_description: str) -> Dict:
    """
    Enhanced match score calculation using Diana's semantic similarity.
    
    Args:
        resume_content (str): Resume text
        job_description (str): Job description
        
    Returns:
        Dict: Enhanced match score with detailed breakdown
    """
    if DIANA_TOOLS_AVAILABLE:
        try:
            # Use Diana's enhanced similarity
            result = calculate_enhanced_similarity(resume_content, job_description)
            
            return {
                "success": True,
                "match_score": {
                    "overall_score": result['percentage'],
                    "semantic_similarity": result['semantic_similarity'],
                    "keyword_overlap": result['keyword_overlap'],
                    "combined_score": result['combined_score']
                },
                "match_quality": result['recommendation'],
                "priority": result['priority'],
                "model_used": result['model_used'],
                "analysis_type": result['analysis_type']
            }
            
        except Exception as e:
            return {"success": False, "error": f"Enhanced match calculation failed: {str(e)}"}
    
    return {"success": False, "error": "Enhanced tools not available"}

# Test function
def test_integration() -> Dict:
    """Test function to verify all integrations work"""
    test_results = {
        "diana_tools_available": DIANA_TOOLS_AVAILABLE,
        "functions_available": [],
        "test_status": "success"
    }
    
    if DIANA_TOOLS_AVAILABLE:
        try:
            sample_text = "Python developer with 5+ years experience using Django and AWS"
            cleaned = clean_resume_text(sample_text)
            test_results["functions_available"].append("text_cleaning")
            
            score = calculate_match_score(sample_text, "Looking for Python expert with Django")
            test_results["functions_available"].append("match_scoring")
            test_results["sample_match_score"] = score
            
        except Exception as e:
            test_results["test_status"] = "error"
            test_results["error"] = str(e)
    
    return test_results

if __name__ == "__main__":
    # Test the integration
    result = test_integration()
    print("🧪 Integration Test Results:")
    print(f"Diana's tools available: {result['diana_tools_available']}")
    print(f"Functions working: {result['functions_available']}")
    print(f"Status: {result['test_status']}")
    
    if result.get('sample_match_score'):
        print(f"Sample match score: {result['sample_match_score']:.3f}")