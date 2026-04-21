import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def safe_parse(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except:
        return {
            "decision": "Parsing failed",
            "reason": text,
            "risk": "Unknown",
            "confidence": "Low"
        }

def run_agents(query, context):
    prompt = f"""
You are a senior business strategy consultant (like McKinsey/Bain).

Analyze the query using structured thinking.

Query: {query}

Context:
{context}

Return STRICT JSON:
{{
 "decision": "",
 "reason": "",
 "market_analysis": "",
 "risk": "",
 "recommendation": "",
 "confidence": ""
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        output = response.choices[0].message.content
        return safe_parse(output)

    except Exception as e:
        print("⚠️ Groq error:", e)

        return {
            "decision": "Fallback mode",
            "reason": "Groq API failed",
            "risk": "Limited accuracy",
            "confidence": "Low"
        }