import os
import json
import base64
from datetime import datetime
from PIL import Image
from vision_utils import ask_gpt_vision
from prompt_builder import generate_questions_from_intent
from cross_reasoner import analyze_cross_document_consistency
from response_aggregator import evaluate_results
import fitz  # PyMuPDF
from PIL import Image
import io


def save_temp_file(file):
    os.makedirs("uploads", exist_ok=True)
    filename = f"uploads/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.name}"
    with open(filename, "wb") as f:
        f.write(file.read())
    return filename


def convert_file_to_images(file_path):
    images = []
    if file_path.lower().endswith(".pdf"):
        doc = fitz.open(file_path)
        for page in doc:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            images.append(img)
    else:
        images.append(Image.open(file_path))
    return images


def run_pipeline(intent, typed_files):
    os.makedirs("outputs", exist_ok=True)
    full_trace = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #trace_file = f"outputs/trace_{timestamp}.json"

    requirements = []

    for file, doc_type in typed_files:
        local_path = save_temp_file(file)
        questions = generate_questions_from_intent(intent, doc_type)
        requirements.extend(questions)
        images = convert_file_to_images(local_path)

        for page_num, img in enumerate(images, start=1):
            for question in questions:
                try:
                    response = ask_gpt_vision(img, question)
                    full_trace.append({
                        "source_file": file.name,
                        "doc_type": doc_type,
                        "page": page_num,
                        "prompt": question,
                        "response": response,
                        "image": img
                    })
                except Exception as e:
                    full_trace.append({
                        "source_file": file.name,
                        "doc_type": doc_type,
                        "page": page_num,
                        "prompt": question,
                        "response": f"ERROR: {str(e)}"
                    })

    '''with open(trace_file, "w") as f:
        json.dump([
            {
                "source_file": row["source_file"],
                "doc_type": row["doc_type"],
                "page": row["page"],
                "prompt": row["prompt"],
                "response": row["response"]
            }
            for row in full_trace
        ], f, indent=2)'''

    checklist, page_evidence = evaluate_results(full_trace, requirements)
    final_verdict = analyze_cross_document_consistency(full_trace, checklist, intent)

    return full_trace, checklist, page_evidence, final_verdict