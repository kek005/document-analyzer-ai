import os
import json
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_questions_for_elements(elements: list[str]) -> dict:
    prompt = (
        "For each of the following document fields, generate a specific question that can be answered by a vision model reviewing a scanned document:")
    prompt += "\n\nFields:\n" + "\n".join(elements)
    prompt += "\n\nReturn a JSON dict where key is field and value is the vision prompt."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're a prompt engineer for a document vision agent."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)