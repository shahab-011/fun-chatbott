import os
import sys

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


app = FastAPI(title="Teacher AI API")

cors_origins_raw = os.getenv("CORS_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in cors_origins_raw.split(",") if origin.strip()]
is_wildcard = "*" in allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=not is_wildcard,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_model():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in Render environment variables.")
    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    return ChatGroq(
        model=model_name,
        temperature=0,
        max_tokens=1024,
    )

MODES = {
    "angry": "You are an angry teacher. Respond to the user in an angry tone.",
    "depressed": "You are a depressed teacher. Respond to the user in a depressed tone.",
    "happy": "You are a happy teacher. Respond to the user in a happy tone.",
    "sad": "You are a sad teacher. Respond to the user in a sad tone.",
}

class ChatMessagePayload(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    mode: str
    history: list[ChatMessagePayload] = []

@app.get("/")
def home():
    return {"message": "Teacher AI API is running"}

@app.get("/health")
def health():
    return {"status": "ok", "message": "Teacher AI API is healthy"}

@app.post("/chat")
def chat(request: ChatRequest):
    if request.mode not in MODES:
        return {"response": "Invalid teacher mode."}

    langchain_messages = [SystemMessage(content=MODES[request.mode])]

    for item in request.history:
        if item.role == "user":
            langchain_messages.append(HumanMessage(content=item.content))
        elif item.role in ("ai", "assistant"):
            langchain_messages.append(AIMessage(content=item.content))

    langchain_messages.append(HumanMessage(content=request.message))

    model = get_model()
    response = model.invoke(langchain_messages)

    return {"response": response.content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
