from fastapi import FastAPI

app = FastAPI(title="Local Voice Chatbot")

@app.get("/")
def home():
    return {"message": "Voice chatbot backend is running"}

import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from fastapi import HTTPException
from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(body: ChatRequest):
    question = body.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Please enter a question.")

    payload = {
        "model": "llama3.2:3b",
        "messages": [{"role": "user", "content": question}],
        "stream": False,
    }

    request = Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urlopen(request, timeout=180) as response:
            result = json.load(response)
    except HTTPError as error:
        raise HTTPException(status_code=502, detail=error.read().decode()) from error
    except (URLError, TimeoutError) as error:
        raise HTTPException(
            status_code=503,
            detail="Ollama did not respond. Open Ollama on your laptop and try again.",
        ) from error

    return {"answer": result["message"]["content"]}

from pathlib import Path
from fastapi.staticfiles import StaticFiles

frontend_folder = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/ui", StaticFiles(directory=frontend_folder, html=True), name="frontend")

from functools import lru_cache

from fastapi import UploadFile
from faster_whisper import WhisperModel


@lru_cache(maxsize=1)
def get_speech_model():
    return WhisperModel("small.en", device="cpu", compute_type="int8")


@app.post("/transcribe")
def transcribe(audio: UploadFile):
    model = get_speech_model()
    segments, _ = model.transcribe(audio.file, beam_size=5, vad_filter=False)
    text = " ".join(segment.text.strip() for segment in segments).strip()
    return {"text": text}