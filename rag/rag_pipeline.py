import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"

def generate_answer(query, context_chunks):

    context = "\n\n".join(context_chunks)
    context = context[:1200]

    prompt = f"""
You are an intelligent assistant.

Rules:
- Answer ONLY from the provided context
- Keep answer clear
- Avoid repetition
- If not found say: "Answer not found in document"

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json().get("response", "")

    except Exception as e:
        return f"Error: {str(e)}"