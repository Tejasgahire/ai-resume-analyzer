# AI Resume Analyzer

An AI-powered Resume Analyzer that evaluates resumes using ATS-style scoring, identifies technical skills, matches candidates with suitable job roles, and provides actionable resume insights.

## Features

* PDF Resume Upload
* Automatic Resume Text Extraction
* OCR Fallback for scanned or image-based PDFs
* AI-powered Resume Analysis using Google Gemini
* ATS Score Analysis
* Job Role Matching
* Technical Skills Detection
* Missing Skills Identification
* Resume Strengths and Improvement Insights
* Job Description Matching
* PDF Analysis Report Generation
* JSON Analysis Download
* Interactive Streamlit Web Interface

## Tech Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| Python            | Core development                |
| Streamlit         | Web application interface       |
| Google Gemini API | AI-powered resume analysis      |
| PyPDF             | PDF text extraction             |
| Tesseract OCR     | OCR for scanned resumes         |
| OpenCV            | Image processing                |
| Pandas            | Data processing                 |
| python-dotenv     | Environment variable management |

## How It Works

1. **Upload Resume**
2. **PDF Text Extraction**
3. **OCR Fallback** — used when text extraction is unavailable
4. **Resume Content Processing**
5. **Google Gemini AI Analysis**
6. **ATS and Skill Analysis**
7. **Job Role Matching**
8. **Results and Resume Insights**
9. **PDF / JSON Report**

## Project Structure

```text
ai-resume-analyzer/
│
├── app.py
├── gemini_analyzer.py
├── resume_parser.py
├── ocr_parser.py
├── main.py
├── test_connection.py
├── config/
│   └── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Tejasgahire/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

> Never upload your `.env` file or expose your API key publicly.

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser using the local Streamlit server.

## Analysis Capabilities

The application analyzes resumes across multiple areas:

* ATS compatibility
* Technical skills
* Missing skills
* Suitable job roles
* Resume strengths
* Areas for improvement
* Job description alignment

The analysis is generated based on the content and skills present in the uploaded resume.

## Example Job Roles

The analyzer can identify suitable roles based on the candidate's resume, including:

* Software Engineering Intern
* Junior Python Developer
* Junior Web Developer
* AI/ML Intern
* Junior Java Developer

The matched roles depend on the skills and experience present in the uploaded resume.

## Security

Sensitive files are excluded from version control using `.gitignore`.

The following files are intentionally excluded:

* `.env`
* Personal resume files
* Generated analysis files
* Virtual environments
* Python cache files
* Backup files

## Future Improvements

* Resume-to-job-description similarity scoring
* More detailed ATS evaluation
* Resume section-wise scoring
* AI-powered resume improvement suggestions
* Multiple resume comparison
* Cloud deployment
* User authentication
* Resume version management

## Author

**Tejas Gahire**

MCA Student | AI and Data Analytics Enthusiast | Software Development

Interested in opportunities related to:

* Data Analytics
* Artificial Intelligence
* Machine Learning
* Python Development
* Software Development

## Project

If you find this project useful, consider giving the repository a star on GitHub.
