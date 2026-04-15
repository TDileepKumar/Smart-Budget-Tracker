import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("API KEY:", os.getenv("OPENAI_API_KEY"))

def get_ai_response(question, summary_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a smart financial assistant. Give clear, short, practical advice."
                },
                {
                    "role": "user",
                    "content": f"""
User question:
{question}

Financial summary:
{summary_text}

Give a helpful answer based on this data.
"""
                }
            ],
            temperature=0.5,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI error: {str(e)}"