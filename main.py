from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import answer_question
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Monday.com BI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.middleware("http")
async def add_ngrok_header(request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "Monday.com BI Agent is running!", "version": "1.0"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask_question(query: Query):
    print(f"\n[API] Received question: {query.question}")
    result = answer_question(query.question)
    return result
