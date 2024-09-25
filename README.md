![WhatsApp Image 2024-09-24 at 17 32 45_932849b2](https://github.com/user-attachments/assets/1b30edcd-7901-41f9-9798-7156e0d00fc1)
![WhatsApp Image 2024-09-24 at 17 44 26_1a7a8398](https://github.com/user-attachments/assets/808709b4-709e-4597-8ab0-bc982bde8e90)

You can access this website: http://192.168.1.3
Requirements:
To run this FastAPI-based transcription project, you need to install the following dependencies and frameworks:

 1. FastAPI and Related Tools:
- FastAPI: The core framework for building the API.
- Uvicorn: ASGI server to run FastAPI apps.
- Jinja2: For HTML templating.
- Starlette: For request handling (comes with FastAPI).
- python-multipart: Required for handling file uploads.
- aiofiles: For asynchronous file handling (e.g., saving the uploaded audio file).
  
 2. Whisper and PyTorch:
- transformers: The Hugging Face library that provides the `WhisperForConditionalGeneration` model and `WhisperProcessor`.
- torch: The PyTorch library for handling Whisper's deep learning operations.
- torchaudio: For audio processing (loading and resampling the audio file).

 3. Optional Libraries:
- Pillow: For handling images, if needed for future frontend extensions.
- Jinja2Templates: Provided by FastAPI for rendering HTML.

 Installation Commands:


pip install fastapi uvicorn jinja2 python-multipart aiofiles
pip install torch torchaudio transformers



- **Whisper's specific version**: Whisper models from Hugging Face are accessible through the `transformers` library.


