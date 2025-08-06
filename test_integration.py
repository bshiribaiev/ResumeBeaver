# test_integration.py
"""
Test integration between Diana's enhanced tools and Arsenii's FastAPI backend
"""

import os
import sys

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def test_diana_tools_import():
    """Test if Diana's tools can be imported"""
    print("🧪 Testing Diana's Tools Import...")
    
    try:
        from tools.api_integration import test_integration
        result = test_integration()
        
        print(f"✅ Diana's tools available: {result['diana_tools_available']}")
        print(f"✅ Functions working: {result['functions_available']}")
        
        if result.get('sample_match_score'):
            print(f"✅ Sample match score: {result['sample_match_score']:.3f}")
        
        return result['diana_tools_available']
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_enhanced_functions():
    """Test the enhanced integration functions"""
    print("\n🧪 Testing Enhanced Integration Functions...")
    
    try:
        from tools.api_integration import (
            enhanced_resume_analysis,
            enhanced_job_analysis, 
            enhanced_match_score_calculation
        )
        
        # Test data
        sample_resume = """
        John Smith
        Senior Python Developer
        john@email.com | (555) 123-4567
        
        SKILLS
        Python, Django, FastAPI, AWS, PostgreSQL, React
        
        EXPERIENCE
        Senior Developer at TechCorp (2020-Present)
        - Built web applications using Python and Django
        - Managed AWS cloud infrastructure
        """
        
        sample_job = """
        We're hiring a Senior Python Developer with experience in:
        - Python programming
        - Django or Flask frameworks  
        - Cloud platforms (AWS preferred)
        - Database experience (PostgreSQL)
        - 5+ years experience required
        """
        
        # Test resume analysis
        print("Testing resume analysis...")
        resume_result = enhanced_resume_analysis(sample_resume)
        if resume_result.get('success'):
            print("✅ Resume analysis working")
            print(f"   Skills found: {resume_result.get('skills_analysis', {}).get('total_technical_skills', 0)}")
            print(f"   Contact found: {bool(resume_result.get('contact_info', {}).get('email'))}")
        else:
            print(f"❌ Resume analysis failed: {resume_result.get('error')}")
        
        # Test job analysis
        print("Testing job analysis...")
        job_result = enhanced_job_analysis(sample_job)
        if job_result.get('success'):
            print("✅ Job analysis working")
            print(f"   Skills required: {len(job_result.get('required_skills', []))}")
        else:
            print(f"❌ Job analysis failed: {job_result.get('error')}")
        
        # Test match score
        print("Testing match score calculation...")
        match_result = enhanced_match_score_calculation(sample_resume, sample_job)
        if match_result.get('success'):
            print("✅ Match scoring working")
            print(f"   Match score: {match_result.get('overall_score', 0):.1f}%")
        else:
            print(f"❌ Match scoring failed: {match_result.get('error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced functions test failed: {e}")
        return False

def test_file_structure():
    """Verify the file structure is correct for integration"""
    print("\n🧪 Testing File Structure...")
    
    required_files = [
        'tools/pdf_parser.py',
        'tools/docx_parser.py', 
        'tools/text_cleaner.py',
        'tools/match_score.py',
        'tools/preprocessor.py',
        'tools/api_helpers.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required Diana's tools files present")
        return True

def test_arsenii_api_structure():
    """Check Arsenii's API structure"""
    print("\n🧪 Testing Arsenii's API Structure...")
    
    api_files = [
        'api/main.py',
        'api/routers/upload.py',
        'api/routers/analyze.py',
        'api/routers/optimize.py'
    ]
    
    missing_api_files = []
    for file_path in api_files:
        if not os.path.exists(file_path):
            missing_api_files.append(file_path)
    
    if missing_api_files:
        print(f"❌ Missing API files: {missing_api_files}")
        return False
    else:
        print("✅ All Arsenii's API files present")
        return True

def main():
    """Run all integration tests"""
    print("🦫 ResumeBeaver Integration Test Suite")
    print("=" * 50)
    
    # Test file structure
    files_ok = test_file_structure()
    api_files_ok = test_arsenii_api_structure()
    
    if not (files_ok and api_files_ok):
        print("\n❌ File structure issues detected. Fix missing files first.")
        return
    
    # Test Diana's tools
    tools_available = test_diana_tools_import()
    
    if tools_available:
        enhanced_functions_ok = test_enhanced_functions()
    else:
        print("⚠️ Diana's tools not available - check imports and dependencies")
        enhanced_functions_ok = False
    
    print("\n" + "=" * 50)
    print("🎯 INTEGRATION STATUS SUMMARY:")
    print(f"File Structure: {'✅' if files_ok and api_files_ok else '❌'}")
    print(f"Diana's Tools: {'✅' if tools_available else '❌'}")
    print(f"Enhanced Functions: {'✅' if enhanced_functions_ok else '❌'}")
    
    if files_ok and api_files_ok and tools_available and enhanced_functions_ok:
        print("\n🎉 INTEGRATION SUCCESSFUL!")
        print("Ready to enhance Arsenii's API endpoints with Diana's tools!")
    else:
        print("\n🔧 INTEGRATION NEEDS WORK")
        print("Follow the setup steps to resolve issues.")

if __name__ == "__main__":
    main()