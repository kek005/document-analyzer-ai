import os
import json
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_requirements_from_intent(intent: str) -> dict:
    prompt = (
        f"""
        You are an AI assistant designing a document validation workflow.
        Based on the intent: "{intent}"

        1. List what types of documents are typically required.
        2. For each document type, list the required elements (like name, date, ID number, signature).
        3. Also, list any cross-document checks needed (like matching names).

        Return your result as JSON like:
        {{
          "documents": {{
            "lease": ["tenant_name", "start_end_date"],
            "id": ["name", "expiration_date"]
          }},
          "cross_checks": ["name_match", "id_not_expired"]
        }}
        """
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're a JSON-generating document analysis planner."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=800
    )
    return json.loads(response.choices[0].message.content)