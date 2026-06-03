# 🏥 Medibrief

An AI-powered medical report assistant that helps users understand medical reports through intelligent summarization, multilingual translation, and conversational question-answering.

---

## 🚀 Features

### 🔐 Authentication

* User Registration
* Secure JWT Login
* Protected Routes

### 📄 Medical Report Processing

* Upload PDF Reports
* Automatic Text Extraction
* Report Storage and Management

### 🤖 AI Summary Generation

* Structured Medical Summaries
* Diagnosis Identification
* Key Findings Extraction
* Severity Assessment
* Recommendations Generation

### 🌍 Translation Support

* Translate Report Summaries
* Multi-language Support

### 💬 Chat With Report

* Ask Questions About Reports
* Context-Aware Responses
* Interactive Report Understanding

### 📁 Report Management

* View Report History
* Retrieve Previous Reports
* Delete Reports

---

## 🛠️ Tech Stack

| Category       | Technology               |
| -------------- | ------------------------ |
| Frontend       | HTML, CSS, JavaScript    |
| Backend        | FastAPI                  |
| Database       | MySQL                    |
| ORM            | SQLAlchemy               |
| Authentication | FastAPI Users, JWT       |
| AI Model       | Ollama (Llama 3 / Gemma) |
| Language       | Python                   |

---

## 🏗️ Architecture

```text
Frontend
    │
    ▼
FastAPI Backend
    │
    ├── Authentication
    ├── File Upload
    ├── Report Management
    ├── Summarization
    ├── Translation
    └── Question Answering
    │
    ▼
Ollama
    │
    ▼
Llama 3 / Gemma
    │
    ▼
MySQL Database
```

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/Medibrief.git
cd Medibrief
```

### Create Virtual Environment

```bash
python -m venv medibriefvenv
```

### Activate Virtual Environment

#### Windows

```bash
medibriefvenv\Scripts\activate
```

#### Linux / MacOS

```bash
source medibriefvenv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Setup

Create a MySQL database:

```sql
CREATE DATABASE medibrief;
```

Configure database URL:

```env
DATABASE_URL=mysql+aiomysql://username:password@localhost/medibrief
```

---

## 🤖 Ollama Setup

Install Ollama:

```bash
https://ollama.com
```

Pull a model:

```bash
ollama pull llama3
```

or

```bash
ollama pull gemma
```

Start Ollama:

```bash
ollama serve
```

Verify installation:

```bash
ollama list
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
SECRET=your-secret-key

DATABASE_URL=mysql+aiomysql://username:password@localhost/medibrief

OLLAMA_URL=http://localhost:11434

OLLAMA_MODEL=llama3
```

---

## ▶️ Run Backend

```bash
uvicorn app:app --reload --port 9000
```

Backend:

```text
http://127.0.0.1:9000
```

Swagger Documentation:

```text
http://127.0.0.1:9000/docs
```

---

## 🌐 Run Frontend

Open:

```text
index.html
```

Or use:

```bash
python -m http.server 5500
```

---

## 📸 Workflow

```text
User Login
     │
     ▼
Upload Medical Report
     │
     ▼
Extract Text
     │
     ▼
Generate AI Summary
     │
     ├── Translate Report
     │
     └── Chat With Report
     │
     ▼
Store Report History
```

---

## 🎯 Future Improvements

* Confidence Scores
* Abnormal Value Detection
* Enhanced Translation
* Voice-Based Interaction
* Doctor-Friendly Summaries
* Patient-Friendly Summaries
* Report Comparison

---

## 👨‍💻 Author

**Mateen Momin**

Final Year B.E. Information Technology Project

---

## ⚠️ Disclaimer

This project is intended for educational purposes only.

The generated summaries, translations, and responses should not be considered professional medical advice. Always consult qualified healthcare professionals for diagnosis and treatment decisions.
