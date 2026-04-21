from fastapi import FastAPI
from rag import load_pdf, chunk_text, create_index, build_context
from singleagent import run_agents

app = FastAPI()

# Load data once
pdf_text = load_pdf("data.pdf")
chunks = chunk_text(pdf_text)
index, chunks = create_index(chunks)

@app.get("/")
def home():
    return {"message": "AI Decision Platform Running 🚀"}

@app.get("/decision")
def decision(query: str):
    context = build_context(query, index, chunks)

    if not context:
        context = "No relevant data found."

    context = context[:500]  # control API usage

    result = run_agents(query, context)

    return result