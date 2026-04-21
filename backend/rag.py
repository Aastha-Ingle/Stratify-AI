import os
import requests
import yfinance as yf
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- PDF ----------
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def chunk_text(text, chunk_size=200):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def create_index(chunks):
    embeddings = embedding_model.encode(chunks)
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index, chunks

# ---------- NEWS ----------
def get_news(query):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "pageSize": 3
    }

    try:
        res = requests.get(url, params=params)
        data = res.json()
        articles = data.get("articles", [])

        news_text = ""
        for a in articles:
            news_text += f"{a['title']}. {a['description']}\n"

        return news_text

    except:
        return "No news data"

# ---------- STOCK ----------
def get_stock():
    try:
        stock = yf.Ticker("TSLA")
        data = stock.history(period="1mo")

        change = data["Close"].iloc[-1] - data["Close"].iloc[0]
        trend = "increasing" if change > 0 else "decreasing"

        return f"Stock trend: {trend}, change: {change:.2f}"

    except:
        return "No stock data"

# ---------- RAG ----------
def retrieve_docs(query, index, chunks, k=2):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(query_embedding, k)
    return [chunks[i] for i in indices[0]]

# ---------- MAIN ----------
def build_context(query, index, chunks):
    context = []

    # PDF
    docs = retrieve_docs(query, index, chunks)
    context.extend(docs)

    # News
    news = get_news(query)
    context.append(news)

    # Stock
    stock = get_stock()
    context.append(stock)

    return "\n\n".join(context)