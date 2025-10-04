from gtts import gTTS
import pygame
import os
import uuid

def speak(text: str):
    filename = f"response_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  # wait until done
        continue

    pygame.mixer.quit()
    os.remove(filename)
