from fastapi import FastAPI
from pydantic import BaseModel
import requests
import uuid
import time

app = FastAPI()

OLLAMA_URL = "http://host.docker.internal:11434/api/chat"

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: list[Message]
    stream: bool = False

@app.post("/v1/chat/completions")
def chat_completions(req: ChatRequest):
    ollama_payload = {
        "model": req.model,
        "messages": [{"role": m.role, "content": m.content} for m in req.messages],
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=ollama_payload)
    data = r.json()

    return {
        "id": str(uuid.uuid4()),
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": data["message"]["content"]
                },
                "finish_reason": "stop"
            }
        ]
    }
