# 🚀 Stratify AI — Agentic Decision Intelligence System

Stratify AI is an AI-powered decision engine that combines real-time data, document intelligence, and large language models to generate structured, explainable business insights.

Unlike traditional chatbots, it delivers **data-driven decisions with reasoning, risk analysis, and confidence scoring**, along with real-time market visualization.

---

## 🧠 Problem Statement

Modern decision-making suffers from:
- Fragmented data sources (reports, news, markets)
- Lack of real-time insights
- Generic AI responses without structured reasoning

Stratify AI solves this by integrating **multi-source data + AI reasoning** into a unified system.

---

## 💡 What it does

Ask a question like:

> *“Should I invest in Tesla?”*

Stratify AI will:
- Analyze relevant document context (RAG)
- Fetch real-time market trends (News API)
- Evaluate stock performance (yfinance)
- Generate a structured response:


---

## ✨ Features

- 🔍 Retrieval-Augmented Generation (RAG)
- 📰 Real-time News Integration
- 📈 Stock Market Analysis (yfinance)
- 🧠 Structured AI Decision Outputs
- 🎨 Interactive Dashboard UI
- 📊 Dynamic Stock Charts (Tesla, Apple, Google, Amazon)
- 🧾 Query History Tracking
- ⚡ Efficient Single-Agent Architecture

---

## 🛠️ Tech Stack

| Layer        | Technology |
|-------------|----------|
| Backend      | FastAPI |
| Frontend     | Gradio |
| AI Model     | Groq (LLaMA 3) |
| RAG          | Sentence Transformers + FAISS |
| Data Sources | News API, yfinance |
| Language     | Python |

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Aastha-Ingle/Stratify-AI.git
cd Stratify-AI

cd backend
pip install -r requirements.txt
uvicorn main:app --reload
cd frontend
python app.py
