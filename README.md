# CareerMatch - AI Resume Analyzer

Smart AI-powered resume analyzer that helps you optimize your resume for any job description.

[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Modern-blue)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## ✨ Features

- 📄 **Resume Parsing** - Upload PDF, DOCX, or TXT files
- 🤖 **AI Analysis** - Google Gemini AI analyzes your resume
- 📊 **Match Score** - 0-100 score showing how well you match the job
- 💡 **Smart Feedback** - Strengths, gaps, missing keywords, improvement tips
- 🎨 **Modern UI** - Beautiful dark mode interface, fully responsive
- ⚡ **Fast** - Results in 5-10 seconds

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API Key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourname/careermatch-resume-analyzer.git
cd careermatch-resume-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment**
```bash
# Create .env file
cp .env.example .env
# Edit .env and add your Google Gemini API key
```

4. **Get API Key**
- Go to https://aistudio.google.com/app/apikeys
- Create/copy your API key
- Paste in .env file

5. **Run the app**
```bash
python main.py
```

6. **Open in browser**
   http://localhost:8000


   ## 📖 How to Use

1. Upload your resume (PDF, DOCX, or TXT)
2. Paste the job description
3. Click "Analyze Match"
4. Review the results:
   - **Match Score**: 0-100 percentage
   - **Key Strengths**: What you're good at
   - **Areas to Develop**: Skills you need to add
   - **Missing Keywords**: Important terms to include
   - **How to Improve**: Specific suggestions

## 🏗️ Project Structure
  careermatch/
├── index.html          # Frontend HTML
├── style.css           # Frontend CSS (dark mode)
├── app.js              # Frontend JavaScript
├── main.py             # FastAPI server
├── ai_analyzer.py      # Gemini AI integration
├── resume_parser.py    # PDF/DOCX/TXT parsing
├── cache.py            # Result caching
├── requirements.txt    # Python dependencies
├── .env.example        # Example env variables
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
└── README.md           # This file

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI**: Google Gemini 2.5 Flash API
- **File Parsing**: PyPDF2, python-docx
- **Icons**: Font Awesome 6.4.0

## 🎨 Features Highlight

### Dark Mode
- Eye-friendly dark theme
- Soft pastel colors (sage blue, green, taupe)
- Perfect for long work sessions

### Responsive Design
- Works on desktop, tablet, mobile
- Touch-friendly interface
- Fast loading

### Professional Code
- Clean architecture
- Comprehensive error handling
- Well-documented
- Production-ready

## 🔐 Security

- API keys stored in .env (not committed)
- No sensitive data exposed
- Input validation at every step
- Secure error messages

## 📈 Example Usage

**Input:**
Resume: Python developer, 3 years experience, REST APIs, Flask
Job: Senior Python Developer, 5+ years, FastAPI, Docker, Kubernetes

**Output:**
Match Score: 68/100 (Good)

✓ Strengths: Python skills, API experience
⚠ Gaps: Need more years of experience
💡 Missing: FastAPI, Docker, Kubernetes
→ Improve: Learn FastAPI and containerization

## 📄 Requirements

See `requirements.txt` for all dependencies:
fastapi
uvicorn
python-dotenv
google-generativeai
PyPDF2
python-docx
pydantic
aiofiles

## 🚀 Deployment

### Local Development
```bash
python main.py
# http://localhost:8000
```

### Production Options
- Heroku
- Railway
- Render
- AWS
- Google Cloud
- DigitalOcean

## 🐛 Troubleshooting

**"API key not found"**
- Check .env file exists
- Verify GEMINI_API_KEY is set
- Restart application

**"File upload fails"**
- Check file size
- Verify PDF/DOCX/TXT format
- Check browser console (F12)

**"Results show error"**
- Check API key is valid
- Check backend logs
- Verify network connection

## 📚 Documentation

For more details, see:
- [Setup Guide](./GITHUB_UPLOAD_GUIDE.md)
- [Architecture](./ARCHITECTURE_AND_DATAFLOW.md)
- [UI Design](./MODERN_UI_REFERENCE.md)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push and create pull request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 📞 Contact

- GitHub: github.com/SenTrick16/careermatch-resume-analyzer
- Email: your.email@example.com
- LinkedIn: linkedin.com/in/yourname

## 🎉 Acknowledgments

- Google Gemini API
- FastAPI Framework
- Open source community

---

⭐ **If you find this helpful, please star the repository!**

Made with ❤️ for career optimization
