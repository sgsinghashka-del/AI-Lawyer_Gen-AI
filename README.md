# ⚖️ AI Lawyer — Legal Case Management & AI-Assisted Research Demo

<p align="center">
  <img src="https://raw.githubusercontent.com/sgsinghashka-del/AI-Lawyer_Gen-AI/main/AI%20Laywer%201.png" alt="AI Lawyer Dashboard Screenshot" width="1000" />
</p>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-RAG%20Optional-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![Status](https://img.shields.io/badge/Status-Demo%20Project-orange?style=for-the-badge)](#)

</div>

AI Lawyer is a Streamlit-based legal workflow application built to demonstrate how a legal-tech product can manage case intake, legal knowledge lookup, evidence handling, and basic analytics in a single dashboard.

This project is best understood as a legal operations demo with AI-assisted workflow features rather than a fully autonomous legal advisor. It combines:

- structured legal case entry
- keyword-driven legal section matching
- PDF evidence extraction
- case tracking and scoring
- legal database search
- optional RAG-based legal question answering

The application uses local CSV datasets for quick demo deployment and can be extended with OpenAI + LangChain + Chroma for more advanced retrieval workflows.

---

## Why this project matters

Legal teams and early-stage legal-tech workflows often need to organize:

- client details and case metadata
- evidence uploads and document review
- relevant legal sections / article matching
- case history and tracking
- notice drafting support
- legal database search and analytics

AI Lawyer packages these tasks into a streamlined interface that is simple to run, easy to extend, and useful as a portfolio project or internal prototype.

---

## Deep project analysis

### 1) Core product concept

This repository is not a production-grade legal platform. Instead, it is a practical demo application that simulates a legal case management dashboard used by a small legal workflow or intake team.

The app is designed around a simple user journey:

1. User logs into the system.
2. Inputs client and legal issue details.
3. Uploads a PDF and extracts text from it.
4. Matches the issue against legal categories.
5. Reviews likely legal sections and case risk.
6. Saves the case into a history file.
7. Views analytics and searches the legal dataset.

### 2) Architecture and implementation

The project is intentionally lightweight and uses a local-first architecture:

- Frontend: Streamlit
- Data handling: pandas
- PDF parsing: PyPDF2
- Storage: CSV files (`legal.csv`, `case_history.csv`, `legal_faq.csv`)
- Optional AI layer: OpenAI + LangChain + Chroma for semantic retrieval
- Fallback logic: local keyword-based matching when no API key is configured

This makes the application easy to run in constrained environments and ideal for prototype or educational use.

### 3) What the app actually does

The system supports the following workflow:

- login page with demo credentials
- new case creation form
- legal problem text input
- evidence selection
- PDF upload and extraction
- legal section matching using keyword rules
- legal notice generation based on user inputs
- case history tracking in CSV format
- search and review of legal database records
- analytics on case types and priority

### 4) Data model

The project stores legal and case data in CSV files:

- `legal.csv` contains legal keywords, sections, law types, punishment, court, and action guidance
- `case_history.csv` keeps case summaries and scores
- `legal_faq.csv` stores helpful legal FAQs for knowledge retrieval

This structure is simple enough for experimentation but also a clear example of how legal data can be structured for demo apps.

### 5) Optional GenAI layer

The repository includes `rag_pipeline.py`, which adds a retrieval layer using:

- OpenAI embeddings
- Chroma vector database
- LangChain retriever
- offline fallback lexical retrieval

This means the app can support real AI-assisted legal lookup when `OPENAI_API_KEY` is configured, while still remaining usable offline when it is not.

Important note: the current project is not a full legal AI system with regulated legal advice generation. It is a research-oriented workflow assistant that helps surface relevant legal information and case context. A qualified lawyer must always review final decision-making.

---

## Features

- Admin login screen for demo access
- New legal case creation form
- Client and legal issue capture
- PDF evidence upload and extraction
- Legal section matching using issue description
- Notice generation for the selected case
- Case history tracking and status updates
- Search and filtering of legal records
- Analytics dashboard for case trends
- Optional RAG-powered legal assistant
- Offline mode without OpenAI dependency

---

## Screenshots

<p align="center">
  <img src="https://raw.githubusercontent.com/sgsinghashka-del/AI-Lawyer_Gen-AI/main/AI%20Laywer%201.png" alt="AI Lawyer Dashboard" width="900" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/sgsinghashka-del/AI-Lawyer_Gen-AI/main/AI%20lawyer%20legal%20search.png" alt="Legal Search Screen" width="430" />
  <img src="https://raw.githubusercontent.com/sgsinghashka-del/AI-Lawyer_Gen-AI/main/AI%20Lawyer%20analytics.png" alt="Analytics Dashboard" width="430" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/sgsinghashka-del/AI-Lawyer_Gen-AI/main/AI%20Lawyer%20DATABASE.png" alt="Legal Database View" width="900" />
</p>

---

## Project structure

```text
AI-Lawyer_Gen-AI/
├── app.py                  # Main Streamlit application
├── rag_pipeline.py        # Optional RAG + retrieval logic
├── RAG_SETUP.md           # RAG setup notes
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── legal.csv              # Legal section reference dataset
├── legal_faq.csv          # FAQ-style legal knowledge
├── case_history.csv       # Saved case records
├── AI Laywer 1.png        # Dashboard screenshot
├── AI lawyer legal search.png
├── AI Lawyer analytics.png
├── AI Lawyer DATABASE.png
├── .env.example           # Optional environment variables template
└── .gitignore
```

---

## Tech stack

- Python 3
- Streamlit
- pandas
- PyPDF2
- OpenAI API (optional)
- LangChain
- Chroma

---

## Setup instructions

### 1) Clone the repository

```bash
git clone https://github.com/sgsinghashka-del/AI-Lawyer_Gen-AI.git
cd AI-Lawyer_Gen-AI
```

### 2) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Run the application

```bash
streamlit run app.py
```

### 5) Demo login

Use the following credentials:

- Username: `admin`
- Password: `admin123`

---

## Optional RAG setup

If you want to enable the AI-enhanced legal assistant:

1. Create a `.env` file from `.env.example`.
2. Add your OpenAI key:

```bash
OPENAI_API_KEY=your_api_key_here
```

3. Start the app and use the AI legal assistant flow when available.

When the OpenAI key is not present, the app automatically falls back to an offline lexical retrieval mode using the local CSV data.

---

---

## Future improvements

Possible next steps:

- add role-based user authentication
- switch from CSV to SQLite/PostgreSQL
- use a proper legal document management system
- implement a more advanced legal retrieval pipeline
- add case status workflows and approval steps
- integrate document classification and summarization
- support multi-user collaboration and audit logs

---

## License

This project is intended for educational and demonstration purposes. It is not legal advice and should not be used as a substitute for professional legal consultation.

