import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in .env")

client = OpenAI(api_key=api_key)


def generate_email_reply(incoming_email: str, tone: str, goal: str) -> str:
    prompt = f"""
You are an email reply assistant.

Your task is to write a clear, helpful, and natural email reply.

Incoming email:
{incoming_email}

Tone:
{tone}

Goal:
{goal}

Instructions:
- Write a professional email reply.
- Keep it concise but useful.
- Do not repeat the incoming email.
- Respond naturally like a human.
- If the email sounds urgent, acknowledge it.
- Only return the email reply text, nothing else.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant that writes email replies."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        raise Exception(f"OpenAI email generation failed: {str(e)}")