from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch
import torchaudio
import os
from starlette.requests import Request

app = FastAPI()

# Mount static files like CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 template instance for rendering HTML
templates = Jinja2Templates(directory="templates")

# Declare global variables for the model and processor
model = None
processor = None

# Background task to preload the Whisper model asynchronously
@app.on_event("startup")
async def load_model():
    global model, processor
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")
    processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")


def transcribe_audio(file_path: str) -> str:
    waveform, sample_rate = torchaudio.load(file_path)

    # Ensure the sample rate is 16000 Hz (Whisper's expected sample rate)
    if sample_rate != 16000:
        waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(waveform)

    inputs = processor(waveform.squeeze().numpy(), return_tensors="pt", sampling_rate=16000)

    # Generate transcription without gradients (since we're not training the model)
    with torch.no_grad():
        generated_ids = model.generate(inputs["input_features"])

    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]


@app.get("/", response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/transcribe", response_class=HTMLResponse)
async def transcribe(request: Request, file: UploadFile = File(...)):
    global model
    if model is None:
        return HTMLResponse("Model is still loading, please wait...", status_code=503)

    file_path = f"uploads/{file.filename}"
    os.makedirs('uploads', exist_ok=True)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Perform the transcription
    transcription = transcribe_audio(file_path)

    return templates.TemplateResponse("result.html", {"request": request, "transcription": transcription})
