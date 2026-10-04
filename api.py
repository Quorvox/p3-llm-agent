from fastapi import FastAPI
from pydantic import BaseModel, Field

from agent.bot import answer, kb

app = FastAPI(title="Support agent")


class ChatIn(BaseModel):
    text: str = Field(min_length=1, max_length=500)


@app.post("/api/chat")
def chat(body: ChatIn):
    hits = kb.search(body.text)
    return {"answer": answer(body.text),
            "hits": [{"doc": h["doc"], "score": h["score"]} for h in hits]}


@app.get("/api/health")
def health():
    return {"ok": True, "docs": len(kb.docs)}
