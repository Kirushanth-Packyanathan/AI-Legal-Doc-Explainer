from fastapi import FastAPI, UploadFile, Form
from app.utils import extract_text_from_pdf
from app.ai_pipeline import summarize_document, answer_question
import tempfile
from fastapi.middleware.cors import CORSMiddleware
from markdown import markdown

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize")
async def summarize(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    text = extract_text_from_pdf(tmp_path)
    summary = summarize_document(text)
    html_summary = markdown(summary)
    return {"summary": html_summary}


@app.post("/ask")
async def ask_question(file: UploadFile, question: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    text = extract_text_from_pdf(tmp_path)
    answer = answer_question(text, question)
    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
