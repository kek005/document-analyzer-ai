import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_questions_from_intent(intent: str, file_type: str):
    system_prompt = (
        "You are an intelligent prompt generator for a vision-based document understanding system.\n\n"
        "Given a business goal and a document type, return 3–6 short, clear questions to ask a vision model.\n"
        "These will be used to verify authenticity and compliance. Do not mention 'page'. Just return the questions."
    )

    user_input = f"""
Business Goal: {intent}
Document Type: {file_type}

List the specific questions we should ask a vision model to verify this document.
Be practical and cover what matters most.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3,
        max_tokens=500
    )

    raw = response.choices[0].message.content.strip()
    return [line.lstrip("0123456789.-) ") for line in raw.split("\n") if line.strip()]