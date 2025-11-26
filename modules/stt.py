import os
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer


# Ensure 'data' directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DATA_DIR, exist_ok=True)

# Load Vosk model (downloaded separately)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../model")

if not os.path.exists(MODEL_PATH):
    raise RuntimeError(
        f"Vosk model not found at {MODEL_PATH}. "
        "Download a model from https://alphacephei.com/vosk/models "
        "and extract it into a folder named 'model'."
    )

model = Model(MODEL_PATH)

def listen_and_transcribe():
    """Capture audio and return text using Vosk."""
    recognizer = KaldiRecognizer(model, 16000)

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1
    ) as stream:

        print("🎤 Listening...")

        while True:
            data = stream.read(4000)[0]

            if recognizer.AcceptWaveform(bytes(data)):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()
                if text:
                    return text  # Return as soon as speech is detected
