# tools/resume_info_extractor.py
import re
import logging
from typing import Dict, List, Optional
from datetime import datetime

def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    """
    Extract contact information using regex patterns.
    
    Args:
        text (str): Resume text
        
    Returns:
        Dict: Contact information found
    """
    contact_info = {}
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    contact_info['email'] = emails[0] if emails else None
    
    # Phone pattern (various US formats)
    phone_patterns = [
        r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
        r'(\d{3})\.(\d{3})\.(\d{4})',
        r'(\d{3})-(\d{3})-(\d{4})'
    ]
    
    phone_found = None
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            if isinstance(phones[0], tuple):
                digits = ''.join([d for d in phones[0] if d.isdigit()])
                if len(digits) >= 10:
                    phone_found = f"({digits[-10:-7]}) {digits[-7:-4]}-{digits[-4:]}"
                    break
    contact_info['phone'] = phone_found
    
    # LinkedIn URL
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    linkedins = re.findall(linkedin_pattern, text.lower())
    contact_info['linkedin'] = f"https://{linkedins[0]}" if linkedins else None
    
    # GitHub URL
    github_pattern = r'github\.com/[\w-]+'
    githubs = re.findall(github_pattern, text.lower())
    contact_info['github'] = f"https://{githubs[0]}" if githubs else None
    
    # Extract name (simple approach - first meaningful line)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    potential_name = None
    for line in lines[:3]:
        if (not any(keyword in line.lower() for keyword in ['engineer', 'developer', '@', 'phone', 'email']) 
            and len(line.split()) <= 4 and len(line) > 5):
            potential_name = line
            break
    
    contact_info['name'] = potential_name
    return contact_info

def extract_skills_advanced(text: str) -> Dict[str, List[str]]:
    """
    Extract and categorize skills using comprehensive patterns.
    
    Args:
        text (str): Resume text
        
    Returns:
        Dict: Categorized skills
    """
    skills = {
        'programming_languages': [],
        'frameworks_libraries': [],
        'databases': [],
        'cloud_platforms': [],
        'tools': [],
        'soft_skills': [],
        'all_technical': []
    }
    
    # Programming Languages
    prog_languages = [
        'Python', 'JavaScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust', 
        'Swift', 'Kotlin', 'TypeScript', 'HTML', 'CSS', 'SQL'
    ]
    
    # Frameworks and Libraries
    frameworks = [
        'React', 'Angular', 'Vue', 'Django', 'Flask', 'FastAPI', 'Spring', 'Laravel', 
        'Express', 'Node.js', 'Bootstrap', 'jQuery', 'pandas', 'NumPy'
    ]
    
    # Databases
    databases = [
        'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle'
    ]
    
    # Cloud Platforms
    cloud_platforms = [
        'AWS', 'Azure', 'Google Cloud', 'GCP', 'Docker', 'Kubernetes'
    ]
    
    # Tools
    tools = [
        'Git', 'Jenkins', 'JIRA', 'VS Code', 'Postman'
    ]
    
    # Soft Skills
    soft_skills = [
        'Leadership', 'Communication', 'Teamwork', 'Problem Solving'
    ]
    
    # Extract each category
    skill_categories = {
        'programming_languages': prog_languages,
        'frameworks_libraries': frameworks,
        'databases': databases,
        'cloud_platforms': cloud_platforms,
        'tools': tools,
        'soft_skills': soft_skills
    }
    
    text_lower = text.lower()
    
    for category, skill_list in skill_categories.items():
        for skill in skill_list:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                skills[category].append(skill)
    
    # Combine all technical skills
    technical_categories = ['programming_languages', 'frameworks_libraries', 'databases', 'cloud_platforms', 'tools']
    for category in technical_categories:
        skills['all_technical'].extend(skills[category])
    
    # Remove duplicates
    for category in skills:
        skills[category] = list(set(skills[category]))
    
    return skills

def extract_years_of_experience(text: str) -> List[str]:
    """
    Extract mentions of years of experience.
    
    Args:
        text (str): Resume text
        
    Returns:
        List: Years of experience found
    """
    experience_patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
        r'(\d+)\+?\s*years?\s+(?:in|with)',
        r'over\s+(\d+)\s+years?'
    ]
    
    years_found = []
    for pattern in experience_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        years_found.extend(matches)
    
    return list(set(years_found))

def extract_comprehensive_resume_info(text: str) -> Dict:
    """
    Master function that extracts all available information from resume text.
    
    Args:
        text (str): Cleaned resume text
        
    Returns:
        Dict: Comprehensive resume information
    """
    
    resume_info = {
        'contact_info': extract_contact_info(text),
        'skills': extract_skills_advanced(text),
        'years_experience': extract_years_of_experience(text),
        'metadata': {
            'total_length': len(text),
            'word_count': len(text.split()),
            'extraction_timestamp': datetime.now().isoformat()
        }
    }
    
    return resume_info

# Test function
def test_extraction(sample_text: str = None) -> Dict:
    """Test the extraction functions with sample text."""
    if not sample_text:
        sample_text = """
        John Smith
        Senior Software Engineer
        john.smith@email.com | (555) 123-4567 | linkedin.com/in/johnsmith
        
        PROFESSIONAL SUMMARY
        Experienced software engineer with 8+ years developing web applications using Python, JavaScript, and React.
        
        TECHNICAL SKILLS
        Programming Languages: Python, JavaScript, Java, SQL
        Frameworks: React, Django, Flask, Node.js
        Cloud Platforms: AWS, Azure
        Databases: PostgreSQL, MongoDB, Redis
        
        PROFESSIONAL EXPERIENCE
        Senior Software Engineer | TechCorp Inc. | 2020 - Present
        • Led development of microservices architecture serving 100K+ users
        • Built RESTful APIs using Python/Django and React frontend
        
        Software Developer | StartupCo | 2018 - 2020
        • Developed full-stack applications using JavaScript and Python
        """
    
    print("🧪 Testing Enhanced Resume Extractor")
    print("=" * 50)
    
    result = extract_comprehensive_resume_info(sample_text)
    
    print(f"📞 Contact Info: {result['contact_info']}")
    print(f"💼 Programming Languages: {result['skills']['programming_languages']}")
    print(f"🔧 Frameworks: {result['skills']['frameworks_libraries']}")
    print(f"💾 Databases: {result['skills']['databases']}")
    print(f"☁️  Cloud Platforms: {result['skills']['cloud_platforms']}")
    print(f"⏱️  Years Experience: {result['years_experience']}")
    print(f"📊 Total Technical Skills: {len(result['skills']['all_technical'])}")
    
    return result

if __name__ == "__main__":
    test_extraction()