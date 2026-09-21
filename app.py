from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import ask


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mattbuild.online", "http://localhost:8888"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str


@app.post("/ask")
def ask_endpoint(q: Question):
    return ask(q.question)    