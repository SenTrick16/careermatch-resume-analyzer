from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import tempfile
import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Import custom modules
from resume_parser import ResumeParser
from ai_analyzer import ResumeAnalyzer

# Initialize modules
parser = ResumeParser()
analyzer = ResumeAnalyzer()

# Define request model
class AnalysisRequest(BaseModel):
    resume_text: str
    job_description: str

# Create FastAPI app (ONLY ONCE)
app = FastAPI(title="Resume Job Match Scorer")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ ROUTES ============

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Resume Scorer API is running"}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse resume"""
    try:
        # Validate file type
        valid_extensions = ['pdf', 'docx', 'doc', 'txt']
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension not in valid_extensions:
            return {
                "success": False,
                "error": f"Invalid file type. Supported: {', '.join(valid_extensions)}"
            }
        
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            # Parse resume
            resume_text = parser.parse_resume(tmp_path, file_extension)
            cleaned_text = parser.clean_text(resume_text)
            
            return {
                "success": True,
                "resume_text": cleaned_text[:2000],  # First 2000 chars for preview
                "full_length": len(cleaned_text),
                "message": "Resume uploaded and parsed successfully"
            }
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    except Exception as e:
        return {
            "success": False,
            "error": f"Error parsing resume: {str(e)}"
        }

@app.post("/analyze")
async def analyze_resume(request: AnalysisRequest):
    """Analyze resume vs job description"""
    try:
        result = analyzer.analyze_match(request.resume_text, request.job_description)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"Error analyzing resume: {str(e)}"
        }

# Mount static files
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)