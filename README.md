# 🎓 AI Interview Mentor – FAANG Prep Assistant

An AI-powered Interview Simulation Platform that helps developers prepare for FAANG and product-based company interviews through real-time question generation, answer evaluation, resume analysis, and performance tracking.

---

## 🚀 Overview

**AI Interview Mentor** is a smart interview preparation system that simulates real-world technical interviews using LLMs.  
It acts as an AI interviewer that asks questions, evaluates responses, and provides structured feedback like a real recruiter.

---

## 💡 Key Features

### 🧠 1. AI Chat Interview Mode
- Conversational AI interviewer
- Context-aware responses
- Multi-mode support (HR / DSA / System Design)

### 📊 2. DSA Question Generator & Evaluator
- Generates topic-based coding questions
- Evaluates answers on:
  - Technical Accuracy
  - Communication Skills
  - Optimization Approach

### 📄 3. Resume Analyzer
- Upload resume (PDF / DOCX / TXT)
- AI-powered ATS analysis
- Provides:
  - Strengths
  - Weaknesses
  - Improvement suggestions

### 💻 4. Code Review System
- Paste code and get:
  - Bug detection
  - Optimization suggestions
  - Complexity analysis (Time & Space)

### 📈 5. Performance Analytics
- Tracks user progress over time
- Visual insights for improvement areas

---

## 🛠️ Tech Stack

- Python 🐍
- Streamlit 🎈
- Groq LLM API 🤖
- PyPDF / python-docx
- JSON Parsing & Prompt Engineering
- Temporary File Handling

---

## 🧠 System Architecture

User → Streamlit UI → AI Engine (LLM API) → Evaluation Layer → Analytics Storage → UI Response

---

## 📦 Installation

```bash
git clone https://github.com/your-username/ai-interview-mentor
cd ai-interview-mentor
pip install -r requirements.txt
streamlit run app.py
