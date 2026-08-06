# 🤖 TalentLens AI – Intelligent Resume Screening Agent

> An AI-powered Resume Screening Agent built with **FastAPI** that automatically parses resumes, extracts candidate information, compares resumes with a Job Description (JD), ranks candidates, and generates recruiter-friendly reports.

---

## 📌 Overview

TalentLens AI simplifies the recruitment process by automatically screening resumes against a given Job Description.

The system extracts candidate details, identifies technical skills, compares them with the required job skills, ranks candidates based on relevance, and generates reports for recruiters.

The project is designed with a modular backend architecture and can be executed through both a REST API and a Command Line Interface (CLI).

---

# ✨ Features

- 📄 Resume Parsing (PDF, DOCX, TXT)
- 📑 Job Description Parsing
- 👤 Candidate Information Extraction
  - Email
  - Phone Number
  - Skills
- 🎯 Skill Matching
- 📊 Candidate Ranking
- 🤖 AI Recommendation Engine
- 💡 AI Decision Summary
- 📁 JSON Report Generation
- 📈 CSV Report Generation
- ⚡ FastAPI REST APIs
- 💻 CLI Pipeline Execution
- 📚 Interactive Swagger Documentation

---

# 🏗 Architecture

```text
                 +-----------------------+
                 |   Job Description     |
                 +-----------+-----------+
                             |
                             |
                     JD Parser Service
                             |
                             |
                    Skill Extraction
                             |
                             |
+----------------------------------------------------------+
|                    Resume Upload Folder                  |
+-------------------------+--------------------------------+
                          |
                          |
                   Resume Parser Service
                          |
                          |
               Candidate Information Extraction
                          |
                          |
                 Matching & Ranking Engine
                          |
                          |
        Recommendation + AI Decision Generation
                          |
                          |
              JSON Report & CSV Report Generator
                          |
                          |
                 FastAPI API / CLI Output
```

---

# 📂 Project Structure

```text
TalentLens/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   └── routes/
│   │   │
│   │   ├── core/
│   │   ├── data/
│   │   │   └── skills.txt
│   │   │
│   │   ├── parsers/
│   │   │   ├── resume_parser.py
│   │   │   └── jd_parser.py
│   │   │
│   │   ├── services/
│   │   │   ├── extraction_service.py
│   │   │   ├── jd_service.py
│   │   │   ├── resume_service.py
│   │   │   ├── matching_service.py
│   │   │   ├── recommendation_service.py
│   │   │   ├── decision_service.py
│   │   │   └── report_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── uploads/
│   │   ├── resumes/
│   │   └── job_descriptions/
│   │
│   ├── reports/
│   │
│   ├── run_pipeline.py
│   ├── requirements.txt
│   ├── README.md
│   └── .gitignore
│
└── frontend/ (Optional)
```

---

# ⚙️ Tech Stack

## Backend

- Python 3.13
- FastAPI
- Uvicorn

## Parsing

- pdfplumber
- python-docx

## Data Processing

- Pandas

## Output

- JSON
- CSV

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/MAHANTHESHVINU/talentlens.git
```

Move to backend

```bash
cd talentlens/backend
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 📥 Sample Input

Place the Job Description inside

```text
uploads/job_descriptions/
```

Example

```text
uploads/job_descriptions/software_engineer.txt
```

Place resumes inside

```text
uploads/resumes/
```

Example

```text
uploads/resumes/resume1.pdf
uploads/resumes/resume2.pdf
```

---

# ▶️ Running the REST API

```bash
python -m uvicorn app.main:app --reload
```

Server

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

# ▶️ Running the CLI

```bash
python run_pipeline.py
```

Example Output

```text
======================================================================
TalentLens AI Resume Screening Pipeline
======================================================================

Loading Job Description...
Job Description Loaded

Loading Resumes...
2 Resume(s) Loaded

Analyzing Candidates...

Rank #1

Resume : Software Engineer Resume.pdf

Score : 82%

Recommendation : Strong Match

Matched Skills :

Python

SQL

Git

Docker

Missing Skills :

FastAPI

Machine Learning

Reports Generated

reports/final_report.json

reports/final_report.csv
```

---

# 🌐 API Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | `/` | Project Information |
| GET | `/health/` | Health Check |
| POST | `/upload/resumes` | Upload Resume Files |
| POST | `/analysis/` | Analyze Candidates |
| GET | `/results/` | View Results |

---

# 📊 Output Reports

The system automatically generates

```
reports/

├── final_report.json

└── final_report.csv
```

Example JSON

```json
{
  "filename": "resume.pdf",
  "score": 82,
  "recommendation": "Strong Match",
  "matched_skills": [
    "Python",
    "SQL",
    "Git"
  ],
  "missing_skills": [
    "Docker"
  ]
}
```

---

# 🧠 AI Workflow

```text
Resume
      │
      ▼
Resume Parser
      │
      ▼
Information Extraction
      │
      ▼
Job Description Parser
      │
      ▼
Skill Matching
      │
      ▼
Candidate Ranking
      │
      ▼
Recommendation Engine
      │
      ▼
AI Decision Summary
      │
      ▼
Report Generation
```

---

# ⚖️ Trade-offs

## Current Approach

The current implementation uses a rule-based extraction and keyword-based matching strategy.

This approach was selected because it offers:

- Fast execution
- Easy debugging
- Modular architecture
- Reliable extraction for structured resumes
- Simple deployment without external AI model dependencies

This allowed delivery of a complete, runnable backend within the challenge timeframe.

---

# 🔮 Future Improvements

With additional development time, the following enhancements are planned:

- Semantic resume matching using Sentence Transformers
- LLM-based candidate evaluation
- OCR support for scanned resumes
- Resume section classification
- Recruiter dashboard (React)
- Authentication and role-based access
- Docker containerization
- Database integration
- Cloud deployment (AWS/Azure/GCP)

---

# 📷 Sample Outputs

Include screenshots of:

- Swagger UI
- CLI Execution
- Candidate Ranking
- JSON Output
- CSV Report

---

# 👨‍💻 Author

**Vinumahanthesh G**

Artificial Intelligence & Machine Learning Engineer

GitHub: https://github.com/MAHANTHESHVINU

LinkedIn: https://www.linkedin.com/in/vinumahanthesh

---

# 📄 License

This project was developed as part of the **ROOMAN AI Challenge** for educational and evaluation purposes.