import os
import whisper
import speech_recognition as sr

# Load model
model = whisper.load_model("small")
r = sr.Recognizer()
mic = sr.Microphone()

# Ensure 'data' directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DATA_DIR, exist_ok=True)

def listen_and_transcribe():
    """Capture audio and return transcribed text."""
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    temp_path = os.path.join(DATA_DIR, "temp.wav")
    with open(temp_path, "wb") as f:
        f.write(audio.get_wav_data())

    result = model.transcribe(temp_path)
    return result["text"].strip()
