import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ResumeAnalyzer:
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
    
    def analyze_match(self, resume_text, job_description):
        """Analyze how well resume matches job description"""
        
        prompt = f"""
        Compare the following resume with the job description and provide a detailed analysis.

        RESUME:
        {resume_text}

        JOB DESCRIPTION:
        {job_description}

        Return your response in VALID JSON format (no markdown, no code blocks, pure JSON):

        {{
            "match_score": <number 0-100>,
            "score_explanation": "<brief explanation of the score>",
            "key_strengths": [<list of 3-4 key strengths matching the job>],
            "key_gaps": [<list of 3-4 missing skills or experience>],
            "missing_keywords": [<list of 3-4 important keywords from job description not in resume>],
            "improvement_suggestions": [<list of 4-5 actionable suggestions to improve match>]
        }}

        Make sure all fields are present and the JSON is valid. Return ONLY the JSON, nothing else.
        """

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Remove ```json
            if response_text.startswith("```"):
                response_text = response_text[3:]  # Remove ```
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Remove ```
            
            response_text = response_text.strip()
            
            # Parse JSON response
            analysis = json.loads(response_text)
            
            # Validate required fields
            required_fields = [
                "match_score",
                "score_explanation",
                "key_strengths",
                "key_gaps",
                "missing_keywords",
                "improvement_suggestions"
            ]
            
            for field in required_fields:
                if field not in analysis:
                    return {
                        "success": False,
                        "error": f"Missing required field in response: {field}"
                    }
            
            # Ensure match_score is between 0-100
            analysis["match_score"] = max(0, min(100, int(analysis["match_score"])))
            
            return {
                "success": True,
                "analysis": analysis
            }
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Invalid JSON in API response: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error analyzing resume: {str(e)}"
            }