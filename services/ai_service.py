import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Check your .env file.")

client = OpenAI(api_key=api_key)


def get_ai_response(question, summary_text):
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

    except Exception as e:
        return f"AI error: {str(e)}"