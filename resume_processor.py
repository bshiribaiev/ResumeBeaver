# Unified resume analysis that combines all processing capabilities

from typing import Dict, List, Optional, Set
import re
from sentence_transformers import SentenceTransformer
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Initialize models 
nlp = spacy.load('en_core_web_sm')
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

class ResumeAnalyzer:    
    def __init__(self, use_watson: bool = True):
        self.use_watson = use_watson
        self.watson_client = None
        if use_watson:
            try:
                from watson_client import get_watson_client
                self.watson_client = get_watson_client()
            except:
                logging.warning("Watson client unavailable, using local processing")
    
    # Extract all skills from text with categorization
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        skill_patterns = {
            'languages': [
                'Python', 'JavaScript', 'TypeScript', 'Java', 'C\\+\\+', 'C#', 
                'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin', 'PHP', 'R', 'Scala'
            ],
            'frameworks': [
                'React', 'Angular', 'Vue', 'Django', 'Flask', 'FastAPI', 'Spring',
                'Express', 'Node\\.js', 'Rails', 'Laravel', '.NET', 'Next\\.js'
            ],
            'databases': [
                'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle',
                'DynamoDB', 'Cassandra', 'ElasticSearch', 'Neo4j'
            ],
            'cloud': [
                'AWS', 'Azure', 'GCP', 'Google Cloud', 'Docker', 'Kubernetes',
                'Terraform', 'CloudFormation', 'Heroku', 'DigitalOcean'
            ],
            'tools': [
                'Git', 'GitHub', 'GitLab', 'Jenkins', 'CI/CD', 'JIRA', 'Slack',
                'VS Code', 'IntelliJ', 'Postman', 'Swagger', 'GraphQL', 'REST'
            ]
        }
        
        results = {category: [] for category in skill_patterns}
        results['all'] = []
        text_lower = text.lower()
        
        for category, skills in skill_patterns.items():
            for skill in skills:
                if re.search(r'\b' + skill.lower() + r'\b', text_lower, re.IGNORECASE):
                    results[category].append(skill)
                    results['all'].append(skill)
        
        # Remove duplicates
        for category in results:
            results[category] = list(set(results[category]))
        
        return results
    
    # Extract contact information from resume
    def extract_contact(self, text: str) -> Dict[str, Optional[str]]:
        contact = {}
        
        # Email
        email_match = re.search(r'\b[\w._%+-]+@[\w.-]+\.[A-Z|a-z]{2,}\b', text)
        contact['email'] = email_match.group(0) if email_match else None
        
        # Phone (US format)
        phone_match = re.search(r'(\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})', text)
        if phone_match:
            digits = ''.join(filter(str.isdigit, phone_match.group(0)))
            if len(digits) >= 10:
                contact['phone'] = f"({digits[-10:-7]}) {digits[-7:-4]}-{digits[-4:]}"
        else:
            contact['phone'] = None
        
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/([\w-]+)', text, re.IGNORECASE)
        contact['linkedin'] = f"https://linkedin.com/in/{linkedin_match.group(1)}" if linkedin_match else None
        
        # GitHub
        github_match = re.search(r'github\.com/([\w-]+)', text, re.IGNORECASE)
        contact['github'] = f"https://github.com/{github_match.group(1)}" if github_match else None
        
        return contact
    
    # Calculate comprehensive match score
    def calculate_match_score(self, resume: str, job_desc: str) -> Dict:
        resume_embedding = semantic_model.encode(resume[:1000])
        job_embedding = semantic_model.encode(job_desc[:1000])
        semantic_score = float(cosine_similarity([resume_embedding], [job_embedding])[0][0])
        
        # Skill matching
        resume_skills = set(self.extract_skills(resume)['all'])
        job_skills = set(self.extract_skills(job_desc)['all'])
        
        if job_skills:
            skill_coverage = len(resume_skills & job_skills) / len(job_skills)
            missing_skills = list(job_skills - resume_skills)
        else:
            skill_coverage = 0.0
            missing_skills = []
        
        # Keyword frequency matching using TF-IDF
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=50)
            tfidf_matrix = vectorizer.fit_transform([resume, job_desc])
            keyword_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            keyword_similarity = 0.0
        
        # Calculate weighted overall score
        overall_score = (
            semantic_score * 0.4 +
            skill_coverage * 0.35 +
            keyword_similarity * 0.25
        )
        
        return {
            'overall_score': round(overall_score * 100, 1),
            'semantic_match': round(semantic_score * 100, 1),
            'skill_match': round(skill_coverage * 100, 1),
            'keyword_match': round(keyword_similarity * 100, 1),
            'missing_skills': missing_skills[:10],
            'matching_skills': list(resume_skills & job_skills),
            'recommendation': self._get_recommendation(overall_score)
        }
    
    # Get match recommendation based on score
    def _get_recommendation(self, score: float) -> str:
        if score >= 0.8:
            return "Excellent match - minor tweaks recommended"
        elif score >= 0.6:
            return "Good match - add missing skills and keywords"
        elif score >= 0.4:
            return "Fair match - significant improvements needed"
        else:
            return "Poor match - major changes required"
    
    # Analyze resume with optional AI enhancement
    def analyze_resume(self, resume_text: str) -> Dict:
        skills = self.extract_skills(resume_text)
        contact = self.extract_contact(resume_text)
        
        # Extract experience years
        exp_matches = re.findall(r'(\d+)\+?\s*years?', resume_text, re.IGNORECASE)
        years_experience = max(map(int, exp_matches)) if exp_matches else None
        
        result = {
            'contact_info': contact,
            'skills': skills,
            'years_experience': years_experience,
            'word_count': len(resume_text.split()),
            'ats_score': self._calculate_ats_score(resume_text)
        }
        
        # Add Watson AI status (your client doesn't have analyze_resume method)
        if self.watson_client and self.watson_client.watson_available:
            result['ai_powered'] = True
            result['ai_model'] = "meta-llama/llama-3-1-70b-instruct"
        else:
            result['ai_powered'] = False
        
        return result
    
    # Calculate ATS compatibility score
    def _calculate_ats_score(self, text: str) -> Dict:
        score = 100
        issues = []
        
        # Check for standard sections
        sections = ['experience', 'education', 'skills', 'summary']
        found_sections = sum(1 for s in sections if s in text.lower())
        if found_sections < 3:
            score -= 20
            issues.append("Missing standard section headers")
        
        # Check for contact info
        contact = self.extract_contact(text)
        if not contact.get('email'):
            score -= 15
            issues.append("No email address found")
        if not contact.get('phone'):
            score -= 10
            issues.append("No phone number found")
        
        # Check for problematic characters
        if any(char in text for char in ['•', '→', '★', '◆', '▪']):
            score -= 10
            issues.append("Contains special characters that may confuse ATS")
        
        return {
            'score': max(score, 0),
            'issues': issues,
            'recommendations': self._get_ats_recommendations(issues)
        }
    
    # Generate ATS improvement recommendations
    def _get_ats_recommendations(self, issues: List[str]) -> List[str]:
        recommendations = []
        
        if "Missing standard section headers" in issues:
            recommendations.append("Add clear section headers: Experience, Education, Skills")
        if "No email address found" in issues:
            recommendations.append("Include your email address at the top")
        if "No phone number found" in issues:
            recommendations.append("Add a phone number in standard format")
        if any("special characters" in issue for issue in issues):
            recommendations.append("Replace bullet points with standard dashes (-)")
        
        return recommendations
    
    # Optimize resume for specific job
    def optimize_resume(self, resume: str, job_desc: str) -> Dict:
        match_analysis = self.calculate_match_score(resume, job_desc)
        
        # Extract key terms from job that are missing from resume
        job_doc = nlp(job_desc)
        resume_doc = nlp(resume)
        
        job_keywords = set([token.lemma_.lower() for token in job_doc 
                           if not token.is_stop and token.is_alpha and len(token.text) > 2])
        resume_keywords = set([token.lemma_.lower() for token in resume_doc 
                              if not token.is_stop and token.is_alpha and len(token.text) > 2])
        
        missing_keywords = list(job_keywords - resume_keywords)[:15]
        
        optimization = {
            'match_score': match_analysis,
            'missing_keywords': missing_keywords,
            'missing_skills': match_analysis['missing_skills'],
            'suggestions': self._generate_suggestions(match_analysis),
            'ats_analysis': self._calculate_ats_score(resume)
        }
        
        # Add AI-powered optimization using your Watson client
        if self.watson_client and self.watson_client.watson_available:
            try:
                ai_result = self.watson_client.optimize_resume_content(resume, job_desc)
                if ai_result.get('success'):
                    optimization['ai_suggestions'] = ai_result.get('watson_optimizations', '')
                    optimization['ai_model'] = ai_result.get('model_used', '')
                    optimization['ai_source'] = ai_result.get('source', '')
                    optimization['ai_powered'] = True
                else:
                    optimization['ai_powered'] = False
            except Exception as e:
                logging.error(f"Watson optimization error: {e}")
                optimization['ai_powered'] = False
        else:
            optimization['ai_powered'] = False
        
        return optimization
    
    # Generate improvement suggestions
    def _generate_suggestions(self, match_analysis: Dict) -> List[Dict]:
        suggestions = []
        
        if match_analysis['skill_match'] < 70:
            suggestions.append({
                'category': 'Skills',
                'priority': 'high',
                'suggestion': f"Add missing skills: {', '.join(match_analysis['missing_skills'][:5])}",
                'impact': 'High impact on match score'
            })
        
        if match_analysis['keyword_match'] < 60:
            suggestions.append({
                'category': 'Keywords',
                'priority': 'high',
                'suggestion': 'Incorporate more job-specific terminology throughout your resume',
                'impact': 'Improves ATS ranking'
            })
        
        if match_analysis['semantic_match'] < 70:
            suggestions.append({
                'category': 'Content',
                'priority': 'medium',
                'suggestion': 'Align your experience descriptions with job requirements',
                'impact': 'Better contextual matching'
            })
        
        return suggestions