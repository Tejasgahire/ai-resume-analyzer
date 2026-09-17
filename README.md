\# 🤖 AI Resume Analyzer



An AI-powered Resume Analyzer that evaluates resumes using ATS-style scoring, identifies technical skills, matches candidates with suitable job roles, and provides actionable resume insights.



\## 🚀 Features



\* 📄 PDF Resume Upload

\* 🔍 Automatic Resume Text Extraction

\* 🖼️ OCR Fallback for scanned/image-based PDFs

\* 🤖 AI-powered Resume Analysis using Google Gemini

\* 📊 ATS Score Analysis

\* 💼 Job Role Matching

\* 🛠️ Technical Skills Detection

\* ⚠️ Missing Skills Identification

\* 💡 Resume Strengths \& Improvement Insights

\* 🎯 Job Description Matching

\* 📑 PDF Analysis Report Generation

\* 📥 JSON Analysis Download

\* 🌐 Interactive Streamlit Web Interface



\## 🛠️ Tech Stack



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



\## 🏗️ Project Structure



```text

ai-resume-analyzer/

│

├── app.py

├── gemini\_analyzer.py

├── resume\_parser.py

├── ocr\_parser.py

├── main.py

├── test\_connection.py

├── config/

│   └── config.py

├── requirements.txt

├── .gitignore

└── README.md

```



\## ⚙️ How It Works



```text

Upload Resume

&#x20;     ↓

PDF Text Extraction

&#x20;     ↓

OCR Fallback (if required)

&#x20;     ↓

Resume Content Processing

&#x20;     ↓

Google Gemini AI Analysis

&#x20;     ↓

ATS \& Skill Analysis

&#x20;     ↓

Job Role Matching

&#x20;     ↓

Results \& Resume Insights

&#x20;     ↓

PDF / JSON Report

```



\## 🔧 Installation



\### 1. Clone the repository



```bash

git clone https://github.com/Tejasgahire/ai-resume-analyzer.git

cd ai-resume-analyzer

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



\### 3. Activate the virtual environment



\*\*Windows:\*\*



```bash

venv\\Scripts\\activate

```



\### 4. Install dependencies



```bash

pip install -r requirements.txt

```



\### 5. Configure Gemini API



Create a `.env` file in the project root:



```env

GEMINI\_API\_KEY=your\_gemini\_api\_key

```



> Never upload your `.env` file or expose your API key publicly.



\### 6. Run the application



```bash

streamlit run app.py

```



The application will open in your browser at the local Streamlit address.



\## 📊 Analysis Capabilities



The application analyzes a resume across multiple areas:



\* ATS compatibility

\* Technical skills

\* Missing skills

\* Suitable job roles

\* Resume strengths

\* Areas for improvement

\* Job description alignment



It is designed to help students and job seekers understand how their resume may perform against common job requirements.



\## 🎯 Example Job Roles



The analyzer can identify suitable roles based on the candidate's resume, such as:



\* Software Engineering Intern

\* Junior Python Developer

\* Junior Web Developer

\* AI/ML Intern

\* Junior Java Developer



The matched roles depend on the skills and experience present in the uploaded resume.



\## 🔐 Security



Sensitive files are excluded from version control using `.gitignore`.



The following files should \*\*not\*\* be committed:



\* `.env`

\* Personal resumes

\* Generated analysis files

\* Virtual environments

\* Python cache files



\## 🔮 Future Improvements



\* Resume-to-job-description similarity scoring

\* More ATS evaluation criteria

\* Resume section-wise scoring

\* Resume improvement suggestions

\* Multiple resume comparison

\* Cloud deployment

\* User authentication

\* Resume version management



\## 👨‍💻 Author



\*\*Tejas Gahire\*\*



MCA Student | AI \& Data Analytics Enthusiast | Software Development



Interested in opportunities related to:



\* Data Analytics

\* Artificial Intelligence

\* Machine Learning

\* Python Development

\* Software Development



\## ⭐ Project



If you find this project useful, consider giving the repository a ⭐ on GitHub.



