import streamlit as st
from vision_runner import run_pipeline
from document_classifier import classify_document
from vision_utils import extract_preview_text
from email_utils import send_verification_email
import json


st.set_page_config(page_title="Document Ananyzer AI", layout="wide")
st.title("📄 Document Ananyzer AI — Multi-Document Understanding")

st.markdown("Upload multiple documents (e.g. lease + ID). VisionFlow will validate and cross-check.")

uploaded_files = st.file_uploader(
    "Upload all documents (Lease, ID, Utility Bill, etc.)",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

typed_files = []
if uploaded_files:
    st.subheader("🔍 Auto-Detecting Document Types...")
    for file in uploaded_files:
        with st.spinner(f"Classifying `{file.name}`..."):
            # Read only 2-page preview for classification
            doc_preview_text = extract_preview_text(file, max_pages=2)
            doc_type = classify_document(doc_preview_text, file.name)

        st.markdown(f"✅ `{file.name}` classified as: **{doc_type}**")
        typed_files.append((file, doc_type))


use_case_intent = st.text_area("Enter Use Case Intent", value="Verify lease and ID for Peco electricity utility account creation")
user_email = st.text_input("Enter your email to receive results", placeholder="example@domain.com")
send_email = st.checkbox("📬 Send results to this email")


if st.button("🚀 Verify Documents") and typed_files and use_case_intent:
    with st.spinner("Running VisionFlow Intelligence Pipeline..."):
        results, checklist, page_evidence, final_verdict = run_pipeline(use_case_intent, typed_files)

    # ✅ Final Recommendation (High-level decision first)
    st.markdown("## ✅ Recommendation")
    st.success(final_verdict.get("final_recommendation", "❓ No verdict returned"))


    # Email
    if send_email and user_email:
        try:
            html = f"""
            <h2>✅ Recommendation</h2>
            <p>{final_verdict.get('final_recommendation')}</p>

            <h3>📌 Key Facts</h3>
            <ul>
            {''.join([f"<li><b>{k.replace('_',' ').capitalize()}:</b> {v}</li>" for k, v in final_verdict.get('key_facts', {}).items()])}
            </ul>

            <h3>🧠 Explanation</h3>
            <p>{final_verdict.get('explanation')}</p>
            """
            status = send_verification_email(user_email, "VisionFlow Document Results", html)
            if status == 202:
                st.success("📧 Email sent successfully!")
            else:
                st.error(f"Email failed to send. Status: {status}")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")

    # 🧠 Key Facts (Dynamic display)
    if "key_facts" in final_verdict:
        st.markdown("### 📌 Key Document Facts")
        for k, v in final_verdict["key_facts"].items():
            label = k.replace("_", " ").capitalize()
            st.markdown(f"- **{label}**: {v}")

    # 🧾 Checklist Results
    st.subheader("📋 Final Document Status")
    for item, status in checklist.items():
        st.markdown(f"**{item}**: {status}")

    # 🖼️ Evidence Pages with Responses
    st.subheader("📸 Pages with Evidence")
    shown_pages = set(page_evidence.values())
    for res in results:
        if res["page"] in shown_pages and res.get("response"):
            st.markdown(f"### 📄 {res['source_file']} — Page {res['page']}")
            if "image" in res:
                st.image(res["image"], use_container_width=True)
            st.markdown(f"**Prompt:** {res['prompt']}")
            st.markdown(f"**Response:** {res['response']}")