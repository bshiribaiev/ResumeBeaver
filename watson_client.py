import os
import logging
from typing import Dict, Optional
import requests

# NEW: ensure .env is loaded even if main.py order changes
try:
    from dotenv import load_dotenv  # NEW
    load_dotenv()  # NEW
except Exception:
    pass  # NEW

MODEL_ID    = os.getenv("IBM_MODEL_ID", "ibm/granite-13b-instruct-v2")
API_VERSION = os.getenv("IBM_API_VERSION", "2023-05-29")

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
            logging.info(f"Watson client initialized with API key: {self.api_key[:8]}...")
    
    def get_access_token(self) -> Optional[str]:
        if not self.watson_available:
            return None
            
        try:
            token_url = "https://iam.cloud.ibm.com/identity/token"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            
            # FIXED: Correct grant type format (IBM not IAM)
            data = {
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": self.api_key
            }
            
            logging.info(f"Requesting token from: {token_url}")
            logging.info(f"Using API key: {self.api_key[:8]}...")
            
            response = requests.post(token_url, headers=headers, data=data, timeout=10)
            
            logging.info(f"Token response status: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access_token")
                if access_token:
                    logging.info(f"Successfully got access token: {access_token[:20]}...")
                    return access_token
                else:
                    logging.error("No access token in response")
                    return None
            else:
                logging.error(f"Failed to get Watson token: {response.status_code}")
                logging.error(f"Response body: {response.text}")
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
                logging.warning("No access token - falling back to local analysis")
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
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            payload = {
                "input": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.3,
                    "top_p": 1,
                    "repetition_penalty": 1.05
                },
                "model_id": MODEL_ID,  # Working model!
                "project_id": os.getenv('IBM_PROJECT_ID')
            }
            
            api_url = f"{self.url}/ml/v1/text/generation?version=2023-05-29"
            logging.info(f"Making Watson API call to: {api_url}")
            
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            logging.info(f"Watson API response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logging.info(f"Watson API response: {str(result)[:200]}...")
                
                watson_suggestions = result.get('results', [{}])[0].get('generated_text', '')
                
                if watson_suggestions:
                    return {
                        "success": True,
                        "watson_optimizations": watson_suggestions,
                        "model_used": MODEL_ID,
                        "source": "IBM watsonx.ai"
                    }
                else:
                    logging.error("No generated text in Watson response")
                    return self._fallback_optimization(resume_text, job_description)
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