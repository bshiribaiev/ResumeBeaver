# 🦫 ResumeBeaver

**App for automatic resume analysis and tailoring aligned with job descriptions**

*Developed for IBM TechXchange 2025 Hackathon*

AI-powered resume optimization and job matching platform that helps job seekers tailor their resumes to specific job descriptions for better ATS compatibility and higher match scores.

## 👥 Team & Contributions

### IBM TechXchange 2025 Hackathon Team

| Role | Responsibilities | Team Member |
|------|------------------|-------------|
| **Backend Engineer** | FastAPI endpoints + IBM Watson integration + agent orchestration | **Arsenii** |
| **Agent Developer** | LLM-powered agents (resume optimizer, skill matcher) + React frontend | **Bekbol** |
| **Resume Processing Lead** | Resume parsing (PDF/DOCX) + job-resume matching logic | **Diana** |
| **Frontend/UI Developer** | Streamlit UI for uploads, text input, and resume download | **Jean Carlo** |
| **DevOps + Demo Lead** | Environment setup, deployment, GitHub + presentation/demo prep | **Angus** |

### Key Integrations
- **IBM Watson**: Advanced NLP and AI capabilities (Arsenii)
- **LLM Agents**: Intelligent resume optimization agents (Bekbol)
- **React Frontend**: Modern user interface (Bekbol)
- **Advanced NLP Pipeline**: Semantic analysis and matching (Diana)

## 🏆 IBM TechXchange 2025 Hackathon

This project was developed for the **IBM TechXchange 2025 Hackathon**, leveraging advanced AI and machine learning technologies to solve real-world problems in career development and job matching.

### Hackathon Highlights
- **Problem Statement**: Helping job seekers optimize their resumes for better ATS compatibility and job matching
- **Solution**: AI-powered resume analysis and tailoring platform using semantic understanding
- **Technologies**: FastAPI, spaCy, SentenceTransformers, scikit-learn, and advanced NLP
- **Innovation**: Combines semantic similarity with keyword matching for comprehensive resume optimization

## 🎯 Features

### IBM Technologies & AI Integration
- **IBM Watson X.ai**: Full integration with IBM Granite 13B Instruct v2 model for resume optimization
- **Advanced Resume Processing**: Comprehensive skill extraction across 5 categories (languages, frameworks, databases, cloud, tools)
- **Intelligent Matching Algorithm**: Multi-factor scoring combining skill matching, keyword analysis, and semantic similarity
- **ATS Optimization Engine**: Automated compatibility scoring with specific recommendations
- **Document Generation**: Professional DOCX and ATS-friendly TXT resume creation
- **Real-time Processing**: Instant feedback and optimization suggestions
- **Fallback Architecture**: Graceful degradation when Watson is unavailable

### Core Functionality
- **Resume File Processing**: Upload and parse PDF, DOCX, and TXT resume files
- **Job Description Analysis**: Extract requirements, skills, and key terms from job postings
- **AI-Powered Matching**: Calculate semantic similarity between resumes and job descriptions
- **Resume Optimization**: Get actionable suggestions to improve your resume
- **ATS Compatibility**: Score and optimize for Applicant Tracking Systems

### Technical Capabilities
- **Multi-format Support**: PDF, DOCX, DOC, and plain text files
- **Advanced NLP**: Uses spaCy and SentenceTransformer models for semantic analysis
- **Skill Extraction**: Automatically identifies programming languages, frameworks, tools, and soft skills
- **Contact Information Parsing**: Extracts names, emails, phone numbers, LinkedIn, and GitHub profiles
- **Experience Analysis**: Identifies years of experience and education requirements

## 🏗️ Architecture

```
ResumeBeaver/
├── main.py                    # Main FastAPI application (Arsenii)
├── watson_client.py          # IBM Watson integration (Arsenii)
├── resume_processor.py       # Resume processing logic (Diana)
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── .gitignore               # Git ignore rules
├── frontend/                 # React frontend (Bekbol)
│   ├── streamlit_app.py     # Streamlit demo UI (Jean Carlo)
│   ├── upload.py            # File upload utilities
│   ├── venv/                # Virtual environment
│   ├── src/                 # React source code
│   ├── public/              # Static assets
│   ├── package.json         # Node.js dependencies
│   └── vite.config.js       # Vite bundler configuration
└── __pycache__/             # Python cache files
```

## 🚀 Demo & Presentation

### IBM TechXchange 2025 Submission
- **Live Demo**: Available at http://localhost:8000/docs (when running locally)
- **API Documentation**: Interactive Swagger UI with all endpoints
- **Test Suite**: Comprehensive integration tests included

## 🎥 Demo (YouTube)
[![Watch the demo](https://img.youtube.com/vi/hDErU5Crx1E/maxresdefault.jpg)](https://www.youtube.com/watch?v=hDErU5Crx1E)

*Quick Link:* https://youtu.be/hDErU5Crx1E


### Key Demo Features
1. **File Upload & Analysis**: Upload PDF/DOCX/TXT files for comprehensive parsing and analysis
2. **AI-Powered Job Matching**: Watson-enhanced semantic matching between resumes and job descriptions  
3. **Real-time Optimization**: Instant suggestions using IBM Granite 13B Instruct v2 model
4. **Resume Generation**: Create professional DOCX or ATS-optimized TXT resumes with applied improvements
5. **Interactive Preview**: Before/after comparison showing specific enhancements
6. **ATS Compatibility Scoring**: Real-time scoring with actionable recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bshiribaiev/ResumeBeaver.git
   cd ResumeBeaver
   ```

   > Note: Repository will be renamed to ResumeBeaver soon!

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Set up environment variables** (for Watson AI)
   ```bash
   # Create .env file with your IBM credentials
   IBM_WATSON_API_KEY=your_api_key_here
   IBM_PROJECT_ID=your_project_id_here
   IBM_MODEL_ID=ibm/granite-13b-instruct-v2
   IBM_WATSON_URL=https://us-south.ml.cloud.ibm.com
   LOG_LEVEL=INFO
   ```

5. **Run the FastAPI backend**
   ```bash
   python main.py
   ```

5. **Run the Streamlit demo UI**
   ```bash
   cd frontend
   streamlit run streamlit_app.py
   ```

6. **Run the React frontend** (in a separate terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

7. **Access the application**
   - FastAPI Backend: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Streamlit Demo UI: http://localhost:8501
   - React Frontend: http://localhost:5173

### Testing the Installation

Check if all components are working:
```bash
# Test Python dependencies and Watson connection
python -c "
try:
    from watson_client import get_watson_client
    from resume_processor import ResumeAnalyzer
    client = get_watson_client()
    analyzer = ResumeAnalyzer()
    print('✅ Backend dependencies OK')
    print(f'🤖 Watson AI: {\"Available\" if client.watson_available else \"Fallback mode\"}')
except Exception as e:
    print(f'❌ Error: {e}')
"

# Test API endpoints
curl http://localhost:8000/status

# Test Streamlit UI
cd frontend && streamlit run streamlit_app.py --check

# Test React frontend (if using)
cd frontend && npm test
```

## 📚 API Endpoints

### Core Endpoints
- `GET /` - API information and health status
- `GET /health` - Health check endpoint
- `GET /status` - System status including Watson AI availability

### Resume Processing Endpoints  
- `POST /upload` - Upload resume files (PDF/DOCX/TXT) with comprehensive analysis
- `POST /analyze` - Analyze resume or job description text
- `POST /match` - Calculate match score between resume and job description
- `POST /optimize` - Generate optimization suggestions using Watson AI
- `POST /generate` - Create optimized resume in DOCX or TXT format
- `POST /preview` - Preview optimization improvements before generation

### Example Usage

**Upload and Analyze Resume:**
```bash
curl -X POST "http://localhost:8000/upload" \
     -F "file=@resume.pdf"
```

**Get Match Score with Watson AI:**
```bash
curl -X POST "http://localhost:8000/match" \
     -H "Content-Type: application/json" \
     -d '{
       "resume": "Software Engineer with 5 years Python experience...",
       "job_description": "Looking for Senior Python Developer..."
     }'
```

**Generate Optimized Resume:**
```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "resume": "Your resume text...",
       "job_description": "Target job description...",
       "applicant_name": "John Doe",
       "format": "docx"
     }' \
     --output optimized_resume.docx
```

**Check Watson AI Status:**
```bash
curl http://localhost:8000/status
```

**Streamlit Demo Interface:**
- Navigate to http://localhost:8501
- **4-tab interface**: Upload Resume, Text Analysis, Match Score, Resume Generator
- Interactive file upload with real-time analysis
- Watson AI status indicator in sidebar
- Perfect for hackathon demonstrations and live presentations

## 🛠️ Core Components

### Resume Processing Pipeline
1. **File Upload**: Accept PDF, DOCX, or text files with intelligent parsing
2. **Text Extraction**: Advanced extraction using PyPDF2 and python-docx with table support
3. **Watson AI Analysis**: IBM Granite 13B Instruct v2 model for semantic understanding
4. **Skill Categorization**: 100+ skills across 5 categories (languages, frameworks, databases, cloud, tools)
5. **Contact Parsing**: Email, phone, LinkedIn, GitHub extraction with formatting
6. **ATS Scoring**: Compatibility analysis with specific recommendations

### Intelligent Matching Algorithm
- **Multi-factor Scoring**: Combines skill matching (50%), keyword analysis (30%), and semantic similarity (20%)
- **Watson AI Enhancement**: IBM Granite model provides contextual understanding beyond keyword matching  
- **Skill Gap Analysis**: Identifies missing technical skills and suggests additions
- **Keyword Optimization**: Extracts job-specific terminology for ATS compatibility
- **Experience Alignment**: Matches years of experience and education requirements

### Resume Generation System
- **DOCX Creation**: Professional formatting with proper headers, sections, and styling
- **TXT Generation**: ATS-optimized plain text format with clean structure
- **Automatic Optimization**: Applies missing skills and keywords during generation
- **Before/After Preview**: Visual comparison showing specific improvements
- **Download System**: Direct file delivery with proper content types

### Skills Detection Engine
ResumeBeaver recognizes 100+ technical skills across categories:
- **Programming Languages**: Python, JavaScript, Java, C++, TypeScript, etc.
- **Frameworks**: React, Django, Flask, Angular, Spring, FastAPI, etc.
- **Databases**: MySQL, PostgreSQL, MongoDB, Redis, Oracle, etc.
- **Cloud Platforms**: AWS, Azure, GCP, Docker, Kubernetes, Terraform
- **Development Tools**: Git, Jenkins, JIRA, VS Code, Postman, etc.

## 🔧 Configuration

### Environment Variables
Create a `.env` file for configuration:
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# File Upload Settings
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=uploads

# Model Settings
SIMILARITY_MODEL=all-MiniLM-L6-v2
```

### Logging
Configure logging in your application:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## 📊 Response Examples

### Match Score Analysis Response
```json
{
  "success": true,
  "match_analysis": {
    "overall_score": 78.5,
    "semantic_match": 72.1,
    "skill_match": 85.2,
    "keyword_match": 76.8,
    "missing_skills": ["React", "AWS", "Docker"],
    "matching_skills": ["Python", "FastAPI", "PostgreSQL"],
    "recommendation": "Good match - add missing skills and keywords"
  },
  "timestamp": "2025-08-15T10:30:00"
}
```

### Watson AI Optimization Response
```json
{
  "success": true,
  "optimization": {
    "match_score": {
      "overall_score": 78.5,
      "skill_match": 85.2,
      "keyword_match": 76.8
    },
    "ai_powered": true,
    "ai_model": "ibm/granite-13b-instruct-v2",
    "ai_suggestions": "1. Add React and AWS to skills section\n2. Highlight API development experience\n3. Include containerization experience\n4. Quantify achievements with metrics\n5. Use standard section headers for ATS",
    "missing_skills": ["React", "AWS", "Docker"],
    "missing_keywords": ["microservices", "scalable", "cloud-native"],
    "suggestions": [
      {
        "category": "Skills",
        "priority": "high", 
        "suggestion": "Add these relevant skills: React, AWS, Docker",
        "impact": "High impact on match score"
      }
    ],
    "ats_analysis": {
      "score": 85,
      "issues": [],
      "recommendations": ["Use standard section headers"]
    }
  }
}
```

### Resume Analysis Response  
```json
{
  "success": true,
  "analysis": {
    "contact_info": {
      "email": "john.smith@email.com",
      "phone": "(555) 123-4567",
      "linkedin": "https://linkedin.com/in/johnsmith",
      "github": "https://github.com/johnsmith"
    },
    "skills": {
      "languages": ["Python", "JavaScript", "Java"],
      "frameworks": ["Django", "React", "FastAPI"],
      "databases": ["PostgreSQL", "MongoDB"],
      "cloud": ["AWS", "Docker"],
      "tools": ["Git", "Jenkins"],
      "all": ["Python", "JavaScript", "Django", "React", "AWS"]
    },
    "years_experience": 5,
    "word_count": 450,
    "ats_score": {
      "score": 85,
      "issues": [],
      "recommendations": ["Add phone number", "Use standard headers"]
    },
    "ai_powered": true,
    "ai_model": "ibm/granite-13b-instruct-v2"
  }
}
```

### System Status Response
```json
{
  "status": "operational",
  "version": "2.0.0",
  "features": {
    "file_upload": true,
    "resume_analysis": true,
    "job_analysis": true,
    "match_scoring": true,
    "optimization": true,
    "resume_generation": true,
    "ai_powered": true
  },
  "ai_status": {
    "watson_available": true,
    "model": "ibm/granite-13b-instruct-v2",
    "model_provider": "IBM Watson"
  }
}
```

## 🧪 Testing

### Unit Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_match_score.py

# Run with coverage
pytest --cov=tools --cov-report=html
```

### Integration Tests
```bash
# Test Diana's tools integration
python test_integration.py

# Test API endpoints
python -m pytest tests/test_api.py
```

## 🚧 Development

### Project Structure Guidelines
- `tools/` - Core processing logic (Diana's enhanced tools)
- `api/` - FastAPI application and routers (Arsenii's API)
- `tests/` - Test files
- `docs/` - Documentation
- `uploads/` - Temporary file storage (gitignored)

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Use Black for Python code formatting
- Follow PEP 8 style guidelines
- Add type hints for function parameters and returns
- Include docstrings for all public functions

## 📦 Dependencies

### Core Dependencies
- **FastAPI**: Modern web framework for API development (Backend - Arsenii)
- **IBM Watson X.ai**: AI and NLP services with Granite 13B Instruct v2 model (Backend - Arsenii)  
- **Streamlit**: Interactive demo interface perfect for hackathon presentations (Frontend - Jean Carlo)
- **React + Vite**: Modern frontend framework with fast bundling (Frontend - Bekbol)
- **PyPDF2 & python-docx**: Document processing for resume parsing (Resume Processing - Diana)
- **Advanced Text Processing**: Regex-based skill extraction and contact parsing (Resume Processing - Diana)

### Development Dependencies
- **python-dotenv**: Environment variable management for Watson credentials
- **requests**: HTTP client for Watson API calls
- **Vite**: Fast React development and bundling
- **uvicorn**: ASGI server for FastAPI development

## 🎯 IBM TechXchange 2025 Roadmap

### Hackathon Deliverables ✅
- [x] **AI-powered resume parsing** with 5-category skill classification
- [x] **IBM Watson X.ai integration** using Granite 13B Instruct v2 model
- [x] **Semantic job-resume matching** with multi-factor scoring algorithm
- [x] **Professional resume generation** in DOCX and TXT formats
- [x] **Comprehensive API** with 7 endpoints including file upload and generation
- [x] **Interactive demo interface** with 4-tab Streamlit application
- [x] **Real-time optimization** with before/after preview functionality
- [x] **ATS compatibility analysis** with specific scoring and recommendations
- [x] **Multi-format document support** (PDF, DOCX, TXT) with intelligent parsing

### Future IBM Integration Opportunities
- [ ] **IBM Watson Discovery**: Enhanced job market analytics and trend analysis
- [ ] **IBM Cloud Functions**: Serverless scaling for high-volume resume processing
- [ ] **IBM Db2**: Enterprise data storage for resume analytics and user management
- [ ] **IBM Security**: Advanced data protection and privacy compliance
- [ ] **IBM AI Fairness 360**: Bias detection and fairness in matching algorithms
- [ ] **IBM Natural Language Understanding**: Enhanced sentiment and entity analysis

### Post-Hackathon Development

### Version 1.1 (Upcoming)
- [ ] Real-time resume editing interface
- [ ] Resume template suggestions
- [ ] Industry-specific optimization
- [ ] Batch processing for multiple resumes

### Version 1.2 (Future)
- [ ] AI-powered resume writing assistance
- [ ] Integration with job boards
- [ ] Cover letter optimization
- [ ] Interview preparation suggestions

### Version 2.0 (Long-term)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Machine learning model fine-tuning
- [ ] Enterprise features

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

**File Upload Issues**
- Check file size limits (default: 10MB)
- Verify file formats are supported (PDF, DOCX, DOC)
- Ensure upload directory has write permissions

**Model Loading Errors**
- Verify sentence-transformers installation
- Check internet connection for model download
- Clear model cache if needed

### Performance Optimization
- Use model caching for better performance
- Consider GPU acceleration for large batches
- Implement request rate limiting for production

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- **IBM TechXchange 2025**: For providing the platform and inspiration for this innovation
- **Team Contributions**:
  - **Arsenii**: FastAPI backend architecture, IBM Watson integration, and agent orchestration
  - **Bekbol**: LLM-powered agents development, React frontend, and file organization
  - **Diana**: Enhanced NLP tools, resume parsing pipeline, and matching algorithms
  - **Jean Carlo**: Streamlit UI development and user experience design
  - **Angus**: DevOps setup, deployment, and demo preparation
- **IBM Developer Community**: For resources and Watson SDK documentation
- **Anthropic**: Claude AI assistance in development
- **Hugging Face**: SentenceTransformers models for semantic analysis
- **spaCy**: Advanced NLP capabilities and language models

## 📞 Support

- **Hackathon Questions**: Contact the IBM TechXchange 2025 organizers
- **Technical Issues**: Create an issue on GitHub
- **Documentation**: Check the `/docs` endpoint when running the API
- **Team Contact**: Available during hackathon presentations

---

**🏆 IBM TechXchange 2025 Hackathon Entry**

*Leveraging AI to revolutionize resume optimization and job matching*

**Made with ❤️ by the ResumeBeaver Team**

*Helping job seekers land their dream jobs, one optimized resume at a time.*
