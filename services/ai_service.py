import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


def get_ai_response(question, summary_text):
    if client is None:
        return "AI service is currently unavailable."

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a smart financial assistant. Give short, practical advice."
                },
                {
                    "role": "user",
                    "content": f"""
User question:
{question}

Financial summary:
{summary_text}
"""
                }
            ],
            temperature=0.5,
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return "AI service is currently unavailable."