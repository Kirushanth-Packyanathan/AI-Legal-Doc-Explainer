import logging
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm_api_key = os.environ.get("GOOGLE_API_KEY")

logging.basicConfig(level=logging.INFO)

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    api_key=llm_api_key,
    temperature=0
)

# Summary prompt
SUMMARY_PROMPT = ChatPromptTemplate.from_template("""
You are an AI legal document explainer.
Summarizes the content in simple, easy-to-understand language (no legal jargon).

Highlights important clauses, obligations, or unusual terms that may need attention (e.g., penalties, auto-renewals, one-sided terms).

Flags potential red flags or risks to be aware of.

Allows users to ask specific questions (e.g., “Can I terminate this contract early?”), and get context-based answers from the document.

Optionally provides a confidence level or recommends consulting a lawyer for complex cases.

Document text:
{doc_text}
""")

# Q&A prompt
QA_PROMPT = ChatPromptTemplate.from_template("""
You are an AI legal assistant.
Answer the user's question based only on the document content.
If unsure, say you are unsure and suggest consulting a lawyer.

Document:
{doc_text}

Question:
{question}
""")


def summarize_document(doc_text: str) -> str:
    chain = SUMMARY_PROMPT | llm
    result = chain.invoke({"doc_text": doc_text})
    return result.content if hasattr(result, "content") else str(result)


def answer_question(doc_text: str, question: str) -> str:
    chain = QA_PROMPT | llm
    result = chain.invoke({"doc_text": doc_text, "question": question})
    return result.content if hasattr(result, "content") else str(result)

