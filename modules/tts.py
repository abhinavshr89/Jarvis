import os
import uuid
from gtts import gTTS
import pygame

# Ensure 'data' directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DATA_DIR, exist_ok=True)

def speak(text: str):
    """Convert text to speech and play it using pygame."""
    filename = os.path.join(DATA_DIR, f"response_{uuid.uuid4().hex}.mp3")

    # Generate TTS file
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

    # Play audio
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # Wait until done
        continue

    pygame.mixer.quit()

    # Clean up file after playing
    if os.path.exists(filename):
        os.remove(filename)
