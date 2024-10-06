from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from RAG import query_llm_with_retriever_for_api
app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


origins = [
    "http://localhost:8000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def home():
    return {"message": "Sup G"}


@app.post('/chat')
async def chat(chat_history: List[Message]):
    print(chat_history)
    try:
        completion = await query_llm_with_retriever_for_api(chat_history)
        return {"messages": completion}
    except Exception as e:
        return {"error": str(e)}, 500
