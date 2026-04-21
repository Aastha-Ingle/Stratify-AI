# Stratify AI 🚀

An Agentic AI Decision System that combines:
- RAG (PDF-based knowledge)
- Real-time News API
- Stock Market Data (yfinance)
- LLM reasoning (Groq)

## Features
- Structured decision output (Decision, Risk, Confidence)
- Real-time stock charts
- Interactive dashboard UI
- Multi-source data integration

## Tech Stack
- FastAPI (Backend)
- Gradio (Frontend)
- Groq API (LLM)
- yfinance (Stock data)
- News API

## How to Run

### Backend
cd backend
uvicorn main:app --reload

### Frontend
cd frontend
python app.py