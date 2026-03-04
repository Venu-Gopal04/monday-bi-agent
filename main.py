from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import answer_question
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Monday.com BI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask_question(query: Query):
    result = answer_question(query.question)
    return result

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")