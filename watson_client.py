import os
import logging
from typing import Dict, Optional
import requests

class WatsonXClient:    
    def __init__(self, api_key: str = None, url: str = None):
        """
        Initialize Watson client with credentials
        
        Args:
            api_key: IBM watsonx.ai API key
            url: IBM watsonx.ai service URL
        """
        self.api_key = api_key or os.getenv('IBM_WATSON_API_KEY')
        self.url = url or os.getenv('IBM_WATSON_URL', 'https://us-south.ml.cloud.ibm.com')
        
        if not self.api_key:
            logging.warning("Watson API key not provided - using fallback mode")
            self.watson_available = False
        else:
            self.watson_available = True
    
    def get_access_token(self) -> Optional[str]:
        if not self.watson_available:
            return None
            
        try:
            token_url = "https://iam.cloud.ibm.com/identity/token"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "grant_type": "urn:iam:grant-type:apikey",
                "apikey": self.api_key
            }
            
            response = requests.post(token_url, headers=headers, data=data, timeout=10)
            if response.status_code == 200:
                return response.json().get("access_token")
            else:
                logging.error(f"Failed to get Watson token: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Watson token error: {str(e)}")
            return None
    
    def optimize_resume_content(self, resume_text: str, job_description: str) -> Dict:
        """
        Use Watson AI to optimize resume content for job requirements
        
        Args:
            resume_text: Original resume content
            job_description: Target job description
            
        Returns:
            Dict with optimization suggestions
        """
        if not self.watson_available:
            return self._fallback_optimization(resume_text, job_description)
        
        try:
            access_token = self.get_access_token()
            if not access_token:
                return self._fallback_optimization(resume_text, job_description)
            
            # Create prompt for Llama 3.1 70B
            prompt = f"""
            You are an expert resume optimization assistant. Analyze this resume against the job description and provide specific improvements.

            RESUME:
            {resume_text[:1500]}

            JOB DESCRIPTION:
            {job_description[:1000]}

            Provide 3-5 specific optimization suggestions focusing on:
            1. Keywords to add
            2. Skills to highlight
            3. Experience reframing
            4. ATS improvements

            Format as numbered list with actionable advice.
            """
            
            # Watson API call
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "input": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.3
                },
                "model_id": "meta-llama/llama-3-1-70b-instruct",
                "project_id": os.getenv('IBM_PROJECT_ID', 'd4c90ab0-0522-4eb3-babd-c1bee7f55ca2')
            }
            
            response = requests.post(
                f"{self.url}/ml/v1/text/generation",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                watson_suggestions = result.get('results', [{}])[0].get('generated_text', '')
                
                return {
                    "success": True,
                    "watson_optimizations": watson_suggestions,
                    "model_used": "meta-llama/llama-3-1-70b-instruct",
                    "source": "IBM watsonx.ai"
                }
            else:
                logging.error(f"Watson API error: {response.status_code} - {response.text}")
                return self._fallback_optimization(resume_text, job_description)
                
        except Exception as e:
            logging.error(f"Watson optimization error: {str(e)}")
            return self._fallback_optimization(resume_text, job_description)
    
    def _fallback_optimization(self, resume_text: str, job_description: str) -> Dict:
        return {
            "success": True,
            "watson_optimizations": "Watson AI unavailable - using enhanced local analysis. Key suggestions: 1) Add relevant keywords from job description, 2) Quantify achievements with metrics, 3) Use standard section headers for ATS, 4) Highlight matching skills prominently, 5) Tailor experience descriptions to job requirements.",
            "model_used": "fallback_mode",
            "source": "Local analysis (Watson unavailable)"
        }

# Initialize global Watson client
watson_client = WatsonXClient()

def get_watson_client() -> WatsonXClient:
    return watson_client