import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_cross_document_consistency(vision_trace: list, checklist_summary: dict, intent: str) -> str:
    """
    Combines checklist result and vision trace to produce a grounded final verdict.
    Context-aware: adapts decision strictness based on business intent.
    """

    formatted = {
        "intent": intent,
        "checklist_summary": checklist_summary,
        "vision_responses": [
            {k: v for k, v in row.items() if k != "image"}
            for row in vision_trace
        ]
    }

    system_prompt = (
        "You're a document reasoning expert.\n\n"
    "Your job is to:\n"
    "1. Analyze the checklist and vision responses.\n"
    "2. Return a structured JSON object with:\n"
    "   - 'final_recommendation': One strong sentence on whether the goal can be achieved.\n"
    "   - 'key_facts': A dictionary of the **most relevant facts** found in the documents. You decide which facts matter based on the intent.\n"
    "   - 'explanation': A paragraph explaining your reasoning.\n\n"
    "The output must be valid JSON. Avoid repeating long quotes from the document. Just summarize what matters."
    )

    user_prompt = f"""
Use Case Intent:
{intent}

Checklist Summary:
{json.dumps(checklist_summary, indent=2)}

Vision Model Responses:
{json.dumps(formatted["vision_responses"], indent=2)}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(formatted, indent=2)}
        ],
        temperature=0.3,
        max_tokens=1000
    )

    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return {
            "final_recommendation": response.choices[0].message.content.strip(),
            "key_facts": {},
            "explanation": "❌ Failed to parse structured output. Fallback to raw LLM text."
        }