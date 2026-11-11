# 🤖 TalentLens AI – Intelligent Resume Screening Agent

> A resume-screening application with a **FastAPI** backend and a browser-based recruiter dashboard. Upload a job description and resumes, compare extracted skills, review ranked results, and export reports.

---

## 📌 Overview

TalentLens AI simplifies the recruitment process by automatically screening resumes against a given Job Description.

The system extracts candidate details and skills, compares resumes with the role requirements, ranks candidates, and generates JSON and CSV reports. The dashboard supports PDF, DOCX, and TXT resumes and TXT, PDF, and DOCX job descriptions.

The project can be used through the recruiter dashboard, REST API, or command-line pipeline (CLI).

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

### Analyze files through the API

The multipart endpoint accepts a JD and one or more resumes:

```bash
curl -X POST "http://127.0.0.1:8000/analysis/" \
  -F "job_description=@job_description.txt" \
  -F "resumes=@resume1.pdf" \
  -F "resumes=@resume2.docx"
```

With authentication disabled (the default for local development), you can omit `job_description` or `resumes` to use files already present in the backend upload folders. With authentication enabled, both must be uploaded for each screening and are not retained on the server.

The `POST /upload/resumes` endpoint accepts a multipart `files` field. `GET /analysis/` analyzes files already on disk in local development. `GET /health/` checks API health.

### CLI

Run the pipeline from `backend/` after adding the JD and resumes to the folders above:

```bash
python run_pipeline.py
```

### Deployment notes

The repository includes a Render Blueprint in `render.yaml`, which deploys the FastAPI application and dashboard together on one HTTPS origin:

1. Push the repository to GitHub and create a Render Blueprint deployment from it.
2. Register OAuth web applications with Google and Microsoft. In the Microsoft app registration, allow accounts in any organizational directory and personal Microsoft accounts. Add the deployed service callback URLs as web redirect URIs:
   - `https://<your-render-host>/auth/callback/google`
   - `https://<your-render-host>/auth/callback/microsoft`
3. Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `MICROSOFT_CLIENT_ID`, and `MICROSOFT_CLIENT_SECRET` in the Render service environment. Keep client secrets private; never commit them.
4. Confirm `AUTH_REQUIRED=true` and `SESSION_COOKIE_SECURE=true`. The Blueprint generates `SESSION_SECRET`.
5. Redeploy and open the Render service URL. Sign-in is available to any Google or Microsoft account.

The service can start before provider credentials are configured, but sign-in remains unavailable until they are added. With authentication enabled, analysis and resume-upload endpoints require a signed-in session. Each uploaded JD and resume is parsed from a temporary file and removed after processing; the generated report is returned in the response and is not written to shared report storage. Folder-based analysis is disabled. Upload limits are 10 MB per file and 25 resumes per screening.

Do not make the API publicly usable with `AUTH_REQUIRED=false`. For other hosting providers, serve the frontend and API from the same HTTPS origin where possible. If they use different origins, set `API_BASE` in `frontend/app.js` and set `FRONTEND_ORIGINS` on the API to the exact frontend origin.

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
| GET | `/auth/config` | Sign-in configuration and current user |
| GET | `/auth/login/google` | Start Google sign-in |
| GET | `/auth/login/microsoft` | Start Microsoft sign-in |
| GET | `/auth/callback/{provider}` | OAuth callback |
| POST | `/auth/logout` | Sign out |
| POST | `/upload/resumes` | Upload resume files |
| GET | `/analysis/` | Analyze files from backend upload folders |
| POST | `/analysis/` | Analyze an uploaded JD and resume files (multipart) |
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

Potential future improvements:

- Semantic resume matching using Sentence Transformers
- LLM-based candidate evaluation
- OCR support for scanned resumes
- Resume section classification
- Authentication and role-based access
- Production deployment configuration
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