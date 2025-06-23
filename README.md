# 📄 VisionFlow AI
AI-powered document intake — with eyes and brains.

VisionFlow AI is a vision-native intake engine for document automation.

Instead of parsing text, it sends **each PDF page to GPT-4o Vision** — using custom prompts generated from a simple use-case sentence.

## 🧠 Example

```
Use case: Verify lease is valid for utility setup
→ Generates:
- Does this page contain lease dates?
- Is there a signature box?
- Is the tenant name listed?
→ Sends these to GPT-4o Vision per page
```

## Run It
1. Clone
2. Add `.env` with `OPENAI_API_KEY`
3. Install requirements
```bash
pip install -r requirements.txt
```
4. Launch
```bash
streamlit run app.py
```

🧪 Prompts are generated dynamically from `prompt_builder.py`

📁 Results saved to `outputs/trace_*.json`

---

Built by Jesugnon KEKE — for bleeding-edge AI intake automation

