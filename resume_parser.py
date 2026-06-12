import PyPDF2
from docx import Document
from typing import Optional
import re
import os

class ResumeParser:
    
    def __init__(self):
        pass
    
    def parse_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if len(reader.pages) == 0:
                    raise ValueError("PDF file is empty")
                
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if not text.strip():
                raise ValueError("No text content found in PDF")
            
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def parse_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"DOCX file not found: {file_path}")
        
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            
            if not text.strip():
                raise ValueError("No text content found in DOCX")
            
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    def parse_txt(self, file_path: str) -> str:
        """Read TXT file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"TXT file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            if not text.strip():
                raise ValueError("TXT file is empty")
            
            return text
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")
    
    def parse_resume(self, file_path: str, file_type: str) -> str:
        """Main parsing method with validation"""
        file_type = file_type.lower().strip()
        
        if file_type == 'pdf':
            return self.parse_pdf(file_path)
        elif file_type in ['docx', 'doc']:
            return self.parse_docx(file_path)
        elif file_type == 'txt':
            return self.parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}. Supported: pdf, docx, doc, txt")
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Strip leading/trailing whitespace
        text = text.strip()
        return text