# 🤖 TalentLens AI – Intelligent Resume Screening Agent

> A resume-screening application with a **FastAPI** backend and a browser-based recruiter dashboard. Upload a job description and resumes, compare extracted skills, review ranked results, and export reports.

**Live dashboard:** [talentlens-yn6r.onrender.com](https://talentlens-yn6r.onrender.com/) · **Source code:** [MAHANTHESHVINU/talentlens](https://github.com/MAHANTHESHVINU/talentlens)

---

## 📌 About

TalentLens is a recruiter-style resume screening dashboard. Add a job description and a batch of resumes, then review skill matches, candidate scores, and screening summaries in one place.

This project is a decision-support tool, not an automated hiring decision. Recruiters should review the original resumes and independently assess candidates.

## 🔎 How it works

1. Open the [live dashboard](https://talentlens-yn6r.onrender.com/) and select a JD (`.txt`, `.pdf`, or `.docx`) plus one or more resumes (`.pdf`, `.docx`, or `.txt`).
2. Select **Screen resumes**. The browser uploads the files to the FastAPI service and shows upload and analysis progress.
3. The service extracts readable text and candidate details, identifies skills, compares resume skills with JD skills, calculates match scores, and ranks candidates.
4. Review the dashboard summary, charts, ranked candidate table, and each candidate's detail modal.
5. In the hosted public app, uploads are handled temporarily and are not written to shared upload folders or report storage. Results are returned to the browser for that screening; they are not saved as a shared history.

Uploads are limited to 10 MB per file and 25 resumes per screening. The Render free instance can sleep when idle, so the first request after inactivity may take longer to start.

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
- 📊 Recruiter dashboard with candidate rankings and match charts
- 🌓 Light and dark themes
- 👤 Candidate detail modal with matched and missing skills
- ⬆️ Multi-resume upload with upload and analysis progress

The matching pipeline currently uses rule-based extraction and keyword/skill matching. Treat scores and recommendations as screening signals, not objective measures of candidate quality.

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
│   │   │       └── auth.py
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
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── render.yaml
└── README.md
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

# 📥 Sample Input and File Formats

For CLI or folder-based API analysis, place a job description inside

```text
backend/uploads/job_descriptions/
```

Supported job description formats: `.txt`, `.pdf`, and `.docx`.

```text
backend/uploads/job_descriptions/software_engineer.txt
```

Place resumes inside `backend/uploads/resumes/`. Supported resume formats are `.pdf`, `.docx`, and `.txt`.

```text
backend/uploads/resumes/resume1.pdf
backend/uploads/resumes/resume2.docx
```

---

# ▶️ Running the REST API and Dashboard

From the repository root, install the backend dependencies and start the application:

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

FastAPI serves the dashboard and API from one origin:

- Dashboard: `http://127.0.0.1:8000/`
- API documentation: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health/`

From the dashboard, choose one JD and one or more resumes, then select **Screen resumes**. The result view includes candidate counts, average match, highest match, skill coverage, ranked candidates, and candidate details. Use **Refresh results** to run analysis on the files already in the backend upload folders.

The dashboard also provides a light/dark theme toggle; the selection is saved in the browser.

The dashboard's **About** link opens the source repository on GitHub.

### Analyze files through the API

The multipart endpoint accepts a JD and one or more resumes:

```bash
curl -X POST "http://127.0.0.1:8000/analysis/" \
  -F "job_description=@job_description.txt" \
  -F "resumes=@resume1.pdf" \
  -F "resumes=@resume2.docx"
```

With local persistence enabled, you can omit `job_description` or `resumes` to use files already present in the backend upload folders. When persistence is disabled, both must be uploaded for each screening and are not retained on the server.

The `POST /upload/resumes` endpoint accepts a multipart `files` field. `GET /analysis/` analyzes files already on disk in local development. `GET /health/` checks API health.

### CLI

Run the pipeline from `backend/` after adding the JD and resumes to the folders above:

```bash
python run_pipeline.py
```

### Deployment notes

The [Render Blueprint](./render.yaml) deploys the FastAPI application and dashboard together on one HTTPS origin, without a sign-in screen. `AUTH_REQUIRED=false` makes the app and analysis API public. `PERSIST_SCREENING_DATA=false` ensures uploaded JDs and resumes are parsed from temporary files and not saved to shared upload or report storage. Folder-based analysis is disabled; upload a JD and at least one resume for every screening. Upload limits are 10 MB per file and 25 resumes per screening.

Because there is no sign-in, anyone who can reach the site can submit files and use the screening service. Do not upload confidential resumes unless you are comfortable with that public access model. For other hosting providers, serve the frontend and API from the same HTTPS origin where possible. If they use different origins, set `API_BASE` in `frontend/app.js` and set `FRONTEND_ORIGINS` on the API to the exact frontend origin.

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
| GET | `/` | Dashboard |
| GET | `/api` | Project Information |
| GET | `/health/` | Health Check |
| POST | `/upload/resumes` | Upload resume files |
| GET | `/analysis/` | Analyze files from backend upload folders |
| POST | `/analysis/` | Analyze an uploaded JD and resume files (multipart) |
| GET | `/results/` | View Results |

---

# 📊 Output Reports

When running locally with persistence enabled, the pipeline writes

```
backend/reports/

├── final_report.json

└── final_report.csv
```

The hosted dashboard does not retain uploaded files or write shared reports. Its analysis endpoint returns the report data directly in the response.

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

Potential future improvements:

- Semantic resume matching using Sentence Transformers
- LLM-based candidate evaluation
- OCR support for scanned resumes
- Resume section classification
- Optional authentication and role-based access for private deployments
- Database integration
- Cloud deployment options beyond Render

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