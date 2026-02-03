from fastapi import FastAPI
from pydantic import BaseModel
import requests
import uuid
import time

app = FastAPI()

PRIVATE_IP = "192.168.2.199"
OLLAMA_URL = "http://"+PRIVATE_IP+":11434/api/chat"

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: list[Message]
    stream: bool = False

# モデル一覧を取得　OllamaサーバーのOpenAI-API互換機能を使って取得したものをそのまま流すだけ
@app.get("/v1/models")
def list_models():
    r = requests.get("http://" + PRIVATE_IP + ":11434/v1/models")
    return r.json()

@app.post("/v1/chat/completions")
def chat_completions(req: ChatRequest):
    # ユーザープロンプトをオーバーライドしてみる
    #req.messages[len(req.messages)-1].content = "ピサの斜塔について解説して"

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
