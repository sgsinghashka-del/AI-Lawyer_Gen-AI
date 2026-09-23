# ⚖️ AI Lawyer — AI-Assisted Legal Case Management

<p align="center">
  <img src="https://raw.githubusercontent.com/sgsinghashka-del/AI-Lawyer_Gen-AI/main/AI%20Laywer%201.png" alt="AI Lawyer Dashboard" width="1000" />
</p>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)](#license)
[![Status](https://img.shields.io/badge/Status-Portfolio%20Project-orange?style=for-the-badge)](#)

</div>

AI Lawyer is a Streamlit-based legal case management application designed to help users organize legal cases, manage evidence, search a structured legal database, and generate draft legal notices using a simple AI-assisted workflow.

This project is built as a practical demo for legal-tech workflows, combining case tracking, PDF text extraction, keyword-based legal matching, and analytics in a single easy-to-use dashboard.

---

## Why this project?

Legal work often involves:
- tracking client and case information
- uploading and reviewing evidence
- matching cases with relevant legal sections
- searching previous case records
- drafting initial legal notices

AI Lawyer brings these tasks into one streamlined interface to make legal case handling easier, cleaner, and more structured.

---

## ✨ Key Features

- Secure login screen for demo access
- New case creation with case metadata
- Client and legal problem entry
- PDF evidence upload and text extraction
- Legal section matching using user-entered problem descriptions
- Draft legal notice generation
- Case history tracking
- Legal database search and download
- Interactive analytics dashboard
- User-friendly Streamlit interface

---

## 🧠 AI / GenAI Note

This project is best described as an AI-assisted legal workflow application rather than a full LLM-powered GenAI system.

It currently includes:
- keyword-based legal matching
- PDF text extraction
- structured legal database search
- analytics and scoring
- workflow automation for legal case intake

It does not currently use:
- OpenAI API
- Gemini API
- Claude API
- LangChain
- vector databases
- embeddings
- RAG pipeline

A future version could evolve into a true GenAI + Retrieval-Augmented Generation legal assistant.

---

## 🏗️ Workflow

```mermaid
flowchart TD
    A[Login] --> B[Dashboard]
    B --> C[New Case]
    B --> D[Legal Search]
    B --> E[Case History]
    B --> F[Analytics]

    C --> G[Client Details]
    G --> H[PDF Evidence Upload]
    H --> I[Text Extraction]
    G --> J[Legal Match Engine]
    J --> K[Relevant Legal Sections]
    C --> L[Legal Notice Draft]
    E --> M[Stored Case Records]
    F --> N[Case Insights]
