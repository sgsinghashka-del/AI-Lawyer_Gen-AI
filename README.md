# ⚖️ AI Lawyer — Legal Case Management & AI-Assisted Legal Search

AI Lawyer is a Streamlit-based legal case management application designed to help users organize legal cases, search a structured legal database, extract text from PDF evidence, generate legal notice drafts, and analyze case information through an interactive dashboard.

> **Project Type:** Data Science / AI-Assisted Legal Application
> **Interface:** Streamlit
> **Data Storage:** CSV
> **Document Processing:** PyPDF2
> **Status:** Portfolio / Educational Project

---

## 📌 Project Overview

AI Lawyer provides a simple digital workspace for managing legal cases and searching legal information.

The application allows users to:

* Create and manage legal cases
* Enter client and case information
* Upload PDF evidence
* Extract text from PDF documents
* Search a structured legal database
* Match legal information against a user's legal problem
* Generate a draft legal notice
* Maintain case history
* Analyze cases using an interactive dashboard
* View legal database records
* Download legal database data

The project demonstrates how Python, Streamlit, structured datasets, document processing, search logic, and analytics can be combined into a practical legal-domain application.

---

# 🚀 Key Features

## 1. 🔐 Login System

The application provides a basic login interface before users can access the dashboard.

---

## 2. 📁 New Case Management

Users can create a new legal case by entering:

* Client name
* Mobile number
* Case type
* Priority
* Legal problem
* Evidence/details
* PDF documents

The application generates a case ID and stores the case information in the case history dataset.

---

## 3. 📄 PDF Evidence Processing

Users can upload PDF documents as evidence.

The application uses **PyPDF2** to extract readable text from uploaded PDF files.

This allows extracted document information to become part of the case-processing workflow.

---

## 4. 🔎 Legal Search

Users can search the structured legal database using legal keywords or problem descriptions.

The system compares the entered legal problem with information stored in `legal.csv` and displays matching legal records.

---

## 5. ⚖️ Legal Notice Draft Generation

The application generates a draft legal notice using the information entered for the case.

The generated notice can include:

* Client information
* Case type
* Legal problem
* Evidence information
* Case details

This provides a starting point for preparing a legal document.

---

## 6. 📚 Case History

Previously created cases are stored in:

```text
case_history.csv
```

Users can view historical cases and filter them according to their status.

---

## 7. 📊 Analytics Dashboard

The application provides basic case analytics such as:

* Total number of cases
* Average case score
* Highest case score
* Cases by case type
* Cases by priority

This gives a simple overview of the stored case data.

---

## 8. 🗃️ Legal Database

The application provides access to the structured legal dataset stored in:

```text
legal.csv
```

Users can view and download the legal database.

---

# 🧠 AI / GenAI Explanation

### Current implementation

The current version of this project is primarily an **AI-assisted legal application**, rather than a full Large Language Model (LLM)-based GenAI system.

The current intelligent workflow includes:

```text
User Legal Problem
        ↓
Keyword Matching
        ↓
Legal Database Search
        ↓
Matching Legal Records
        ↓
Case Processing
        ↓
Legal Notice Draft
```

The application also processes uploaded PDF documents and extracts their text for use in the case workflow.

### Important distinction

The current version does **not** directly use:

* OpenAI API
* Gemini API
* Claude API
* Llama
* LangChain
* Vector databases
* Embedding models
* Retrieval-Augmented Generation (RAG)
* An LLM-based answer-generation pipeline

Therefore, the current implementation should not be represented as a fully LLM-powered GenAI application.

### Future GenAI Architecture

A future version can introduce a genuine GenAI/RAG pipeline:

```text
User Question
      ↓
Document Processing
      ↓
Text Chunking
      ↓
Embeddings
      ↓
Vector Database
      ↓
Relevant Legal Documents
      ↓
LLM
      ↓
Grounded Legal Response
      ↓
Source References
```

Possible future technologies include:

* LLM APIs
* Embedding models
* FAISS / Chroma
* LangChain or similar orchestration frameworks
* RAG
* Prompt engineering
* Document retrieval
* Citation/source tracking

This would transform the project from an AI-assisted rule-based application into a more complete **GenAI + RAG legal assistant**.

---

# 🛠️ Technology Stack

| Technology | Purpose                     |
| ---------- | --------------------------- |
| Python     | Application development     |
| Streamlit  | Web application interface   |
| Pandas     | Data processing             |
| PyPDF2     | PDF text extraction         |
| CSV        | Legal and case data storage |
| Git        | Version control             |
| GitHub     | Source-code hosting         |

---

# 📂 Project Structure

```text
AI Lawyer/
│
├── app.py
├── legal.csv
├── case_history.csv
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
    ├── login.png
    ├── dashboard.png
    ├── legal_search.png
    └── analytics.png
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/sgsinghashka-del/AI-Lawyer_Gen-AI.git
```

## 2. Open the project directory

```bash
cd AI-Lawyer_Gen-AI
```

## 3. Create a virtual environment

### Windows

```bash
python -m venv venv
```

## 4. Activate the virtual environment

```bash
venv\Scripts\activate
```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Start Streamlit using:

```bash
streamlit run app.py
```

The application will open in your browser.

If it does not open automatically, Streamlit will display a local URL in the terminal.

---

# 🔑 Demo Login

For the current portfolio/demo implementation:

```text
Username: admin
Password: admin123
```

> For a production application, credentials should be stored securely using environment variables or Streamlit Secrets rather than hard-coded in source code.

---

# 🖼️ Screenshots

## Login Page

## Dashboard

## Legal Search

## Analytics



> Add the screenshots to the `screenshots` folder before publishing the README.

---

# 🔄 Application Workflow

```text
                    ┌──────────────────┐
                    │     Login        │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │    Dashboard     │
                    └────────┬─────────┘
                             ↓
        ┌────────────────────┼────────────────────┐
        ↓                    ↓                    ↓
   New Case            Legal Search          Case History
        ↓                    ↓                    ↓
   PDF Upload          Legal Database       Stored Cases
        ↓                    ↓                    ↓
   Text Extraction     Keyword Matching       Analytics
        ↓                    ↓
   Case Processing     Legal Results
        ↓
   Notice Draft
```

---

# 🔮 Future Improvements

The project can be extended with:

* LLM-powered legal question answering
* Retrieval-Augmented Generation (RAG)
* Vector database integration
* Semantic search
* Legal document embeddings
* Source/citation generation
* Conversation memory
* Multi-document analysis
* Secure authentication
* PostgreSQL/MySQL database
* Cloud deployment
* Role-based access control
* Automated legal document summarization
* Multilingual legal assistance

---

# 🔒 Security Considerations

This project is currently designed as a portfolio/educational application.

For production use, the following should be implemented:

* Secure authentication
* Password hashing
* Environment variables / secrets
* Database-based storage
* Access control
* Encryption of sensitive documents
* Secure document upload validation
* Audit logging
* Removal of personal client information from public datasets

---

# ⚠️ Legal & Educational Disclaimer

This project is developed for **educational, demonstration, and portfolio purposes only**.

It is not a substitute for advice from a qualified lawyer or other licensed legal professional.

The legal information, search results, generated drafts, case scores, and other outputs produced by this application should not be treated as professional legal advice or as a definitive interpretation of applicable law.

Users should independently verify legal information and consult a qualified legal professional before making legal decisions or taking legal action.

---

# 👨‍💻 Author

**Ashka Singh**

GitHub:

https://github.com/sgsinghashka-del

---

# 📌 Repository

GitHub Repository:

https://github.com/sgsinghashka-del/AI-Lawyer_Gen-AI
