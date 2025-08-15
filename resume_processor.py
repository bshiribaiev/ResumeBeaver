# Minimal resume analysis that works without problematic ML libraries

from typing import Dict, List, Optional, Set
import re
import logging

class ResumeAnalyzer:    
    def __init__(self, use_watson: bool = True):
        self.use_watson = use_watson
        self.watson_client = None
        if use_watson:
            try:
                from watson_client import get_watson_client
                self.watson_client = get_watson_client()
            except Exception as e:
                logging.warning(f"Watson client unavailable: {e}")
    
    # Extract all skills from text with categorization
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        skill_patterns = {
            'languages': [
                'Python', 'JavaScript', 'TypeScript', 'Java', 'C\\+\\+', 'C#', 
                'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin', 'PHP', 'R', 'Scala',
                'HTML', 'CSS', 'SQL', 'NoSQL', 'GraphQL', 'C', 'Perl', 'Shell'
            ],
            'frameworks': [
                'React', 'Angular', 'Vue', 'Django', 'Flask', 'FastAPI', 'Spring',
                'Express', 'Node\\.js', 'Rails', 'Laravel', '.NET', 'Next\\.js',
                'Bootstrap', 'Tailwind', 'jQuery', 'Svelte', 'Nuxt', 'Gatsby'
            ],
            'databases': [
                'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle',
                'DynamoDB', 'Cassandra', 'ElasticSearch', 'Neo4j', 'Firebase',
                'MariaDB', 'CouchDB', 'InfluxDB'
            ],
            'cloud': [
                'AWS', 'Azure', 'GCP', 'Google Cloud', 'Docker', 'Kubernetes',
                'Terraform', 'CloudFormation', 'Heroku', 'DigitalOcean',
                'Vercel', 'Netlify', 'Firebase'
            ],
            'tools': [
                'Git', 'GitHub', 'GitLab', 'Jenkins', 'CI/CD', 'JIRA', 'Slack',
                'VS Code', 'IntelliJ', 'Postman', 'Swagger', 'GraphQL', 'REST',
                'Figma', 'Adobe', 'Photoshop', 'Sketch'
            ]
        }
        
        results = {category: [] for category in skill_patterns}
        results['all'] = []
        text_lower = text.lower()
        
        for category, skills in skill_patterns.items():
            for skill in skills:
                pattern = r'\b' + skill.lower().replace('\\', '\\') + r'\b'
                if re.search(pattern, text_lower, re.IGNORECASE):
                    clean_skill = skill.replace('\\', '')
                    results[category].append(clean_skill)
                    results['all'].append(clean_skill)
        
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
        phone_patterns = [
            r'(\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})',
            r'(\d{3})[-.](\d{3})[-.](\d{4})',
            r'\(?(\d{3})\)?\s*(\d{3})[-.](\d{4})'
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                digits = ''.join(filter(str.isdigit, phone_match.group(0)))
                if len(digits) >= 10:
                    contact['phone'] = f"({digits[-10:-7]}) {digits[-7:-4]}-{digits[-4:]}"
                    break
        
        if 'phone' not in contact:
            contact['phone'] = None
        
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/([\w-]+)', text, re.IGNORECASE)
        contact['linkedin'] = f"https://linkedin.com/in/{linkedin_match.group(1)}" if linkedin_match else None
        
        # GitHub
        github_match = re.search(r'github\.com/([\w-]+)', text, re.IGNORECASE)
        contact['github'] = f"https://github.com/{github_match.group(1)}" if github_match else None
        
        return contact
    
    # Basic keyword extraction (no external dependencies)
    def _extract_keywords_basic(self, text: str) -> Set[str]:
        """Basic keyword extraction"""
        # Common stop words
        stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'have', 'had', 'this', 'they', 'been',
            'their', 'said', 'each', 'which', 'she', 'do', 'how', 'her', 'has',
            'or', 'but', 'what', 'there', 'we', 'you', 'all', 'any', 'can', 'had',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'will',
            'am', 'pm', 'inc', 'llc', 'corp', 'ltd', 'co', 'company'
        }
        
        # Extract words, filter out stop words and short words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = {word for word in words if word not in stop_words and len(word) > 2}
        
        return keywords
    
    # Calculate basic match score without ML libraries
    def calculate_match_score(self, resume: str, job_desc: str) -> Dict:
        # Skill matching
        resume_skills = set(self.extract_skills(resume)['all'])
        job_skills = set(self.extract_skills(job_desc)['all'])
        
        if job_skills:
            skill_coverage = len(resume_skills & job_skills) / len(job_skills)
            missing_skills = list(job_skills - resume_skills)
        else:
            skill_coverage = 0.0
            missing_skills = []
        
        # Basic keyword matching
        resume_keywords = self._extract_keywords_basic(resume)
        job_keywords = self._extract_keywords_basic(job_desc)
        
        if job_keywords:
            keyword_coverage = len(resume_keywords & job_keywords) / len(job_keywords)
        else:
            keyword_coverage = 0.0
        
        # Simple text similarity (word overlap)
        resume_words = set(resume.lower().split())
        job_words = set(job_desc.lower().split())
        
        if job_words:
            word_overlap = len(resume_words & job_words) / len(job_words)
        else:
            word_overlap = 0.0
        
        # Calculate weighted overall score
        overall_score = (
            skill_coverage * 0.5 +
            keyword_coverage * 0.3 +
            word_overlap * 0.2
        )
        
        return {
            'overall_score': round(overall_score * 100, 1),
            'semantic_match': round(word_overlap * 100, 1),
            'skill_match': round(skill_coverage * 100, 1),
            'keyword_match': round(keyword_coverage * 100, 1),
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
    
    # Analyze resume without external ML dependencies
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
            'ats_score': self._calculate_ats_score(resume_text),
            'processing_mode': 'basic'  # Indicate we're using basic processing
        }
        
        # Add Watson AI status
        if self.watson_client and self.watson_client.watson_available:
            result['ai_powered'] = True
            import os
            result['ai_model'] = os.getenv("IBM_MODEL_ID", "ibm/granite-13b-instruct-v2") 
        else:
            result['ai_powered'] = False
        
        return result
    
    # Calculate ATS compatibility score
    def _calculate_ats_score(self, text: str) -> Dict:
        score = 100
        issues = []
        
        # Check for standard sections
        sections = ['experience', 'education', 'skills', 'summary', 'work', 'employment']
        found_sections = sum(1 for s in sections if s in text.lower())
        if found_sections < 2:
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
        problematic_chars = ['•', '→', '★', '◆', '▪', '✓', '✗', '→', '←', '↑', '↓']
        if any(char in text for char in problematic_chars):
            score -= 10
            issues.append("Contains special characters that may confuse ATS")
        
        # Check for proper formatting
        if len(text.split('\n')) < 5:
            score -= 15
            issues.append("Document appears to lack proper line breaks")
        
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
            recommendations.append("Replace bullet points with standard dashes (-) or asterisks (*)")
        if any("line breaks" in issue for issue in issues):
            recommendations.append("Use proper paragraph formatting with clear sections")
        
        return recommendations
    
    # Optimize resume for specific job (simplified version)
    def optimize_resume(self, resume: str, job_desc: str) -> Dict:
        match_analysis = self.calculate_match_score(resume, job_desc)
        
        # Extract keywords that appear in job but not in resume
        job_keywords = self._extract_keywords_basic(job_desc)
        resume_keywords = self._extract_keywords_basic(resume)
        missing_keywords = list(job_keywords - resume_keywords)[:15]
        
        optimization = {
            'match_score': match_analysis,
            'missing_keywords': missing_keywords,
            'missing_skills': match_analysis['missing_skills'],
            'suggestions': self._generate_suggestions(match_analysis),
            'ats_analysis': self._calculate_ats_score(resume),
            'processing_mode': 'basic'
        }
        
        # Add AI-powered optimization using Watson client
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
        
        if match_analysis['overall_score'] < 50:
            suggestions.append({
                'category': 'Overall',
                'priority': 'high',
                'suggestion': 'Consider major revisions to better match this position',
                'impact': 'Significant improvement in application success'
            })
        
        return suggestions