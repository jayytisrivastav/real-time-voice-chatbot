# Local Voice Chatbot

A Python chatbot that runs on a laptop. It supports two workflows: a browser interface for asking questions and an API for turning an uploaded voice recording into text. Both use a local FastAPI backend.

## What works

- **Text chat:** Type a question in the browser. FastAPI sends it to `llama3.2:3b` through Ollama and displays the answer.
- **Speech transcription:** Upload a recording, such as an `.m4a` file from Windows Sound Recorder. `faster-whisper` converts it to text using the `small.en` model on the CPU.

Chat and transcription currently work separately. The next milestone is a microphone button that records a question, shows the transcript for review, and sends it to the chatbot. Spoken replies are also planned.

## Run locally on Windows

Install Python and Ollama. Start Ollama, then download the chat model:

```powershell
ollama pull llama3.2:3b
```

Open PowerShell in the project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn faster-whisper python-multipart av==16.1.0
.\.venv\Scripts\python.exe -m uvicorn src.backend.app:app --reload
```

The first transcription downloads the Whisper model. After the models are downloaded, chat and transcription run locally.

## Try it

- **Chat:** Open `http://127.0.0.1:8000/ui/`, type “What is machine learning?”, and click **Send**.
- **Transcription:** Open `http://127.0.0.1:8000/docs`, expand **POST /transcribe**, click **Try it out**, select a recording, and click **Execute**. The `text` field contains the transcript.

## Testing notes

Tested on Windows with Python 3.13. PyAV is pinned to `16.1.0` because version `19.0.2` caused an audio-decoding error in this setup. A four-second recording was transcribed successfully, though the model heard “machine learning” as “machine loading.” Transcription accuracy remains an area for improvement.

## Project files

- `src/backend/app.py` — FastAPI routes, Ollama chat requests, and speech transcription.
- `src/frontend/index.html` — browser interface for typed questions and answers.
