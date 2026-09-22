# ⚖️ AI Lawyer – GenAI Legal Case Management System

## Project Overview

AI Lawyer is a Streamlit-based legal case management and legal information system.

The application allows users to:

- Create and manage legal cases
- Search legal sections
- Match legal problems with relevant legal sections
- Upload and extract text from PDF documents
- Generate legal notice drafts
- Maintain case history
- Explore the legal database
- View case analytics

## Technologies Used

- Python
- Streamlit
- Pandas
- PyPDF2
- CSV
- HTML/CSS

## Features

### 1. Secure Login
Admin login system for accessing the dashboard.

### 2. New Case Management
Users can enter:

- Client name
- Mobile number
- Case type
- Priority
- Legal problem
- Evidence
- PDF documents

### 3. Legal Section Matching
The system searches the legal database based on keywords provided in the user's legal problem.

### 4. PDF Text Extraction
Users can upload PDF documents and extract their text.

### 5. Legal Notice Generation
The application generates a draft legal notice based on case information.

### 6. Case History
Cases are stored in a CSV-based case history database.

### 7. Analytics
The dashboard provides case statistics and charts.

## Project Structure

AI-Lawyer/
│
├── app.py
├── legal.csv
├── case_history.csv
├── requirements.txt
├── README.md
└── .gitignore

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL