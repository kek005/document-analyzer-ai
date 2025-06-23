from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_document(preview_text, filename="document"):
    prompt = f"""
You are a document classifier. Based on the name and content preview below, identify the document type.

Filename: {filename}
Content Preview:
\"\"\"
{preview_text}
\"\"\"

Respond with only one of:
Lease, ID, Utility Bill, Bank Statement, Insurance Card, Other
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You classify documents by type. Respond with only the type name."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=10
    )

    return response.choices[0].message.content.strip()