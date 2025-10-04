import whisper
import speech_recognition as sr

model = whisper.load_model("small")
r = sr.Recognizer()
mic = sr.Microphone()

def listen_and_transcribe():
    """Capture audio and return transcribed text."""
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    with open("temp.wav", "wb") as f:
        f.write(audio.get_wav_data())

    result = model.transcribe("temp.wav")
    return result["text"].strip()
