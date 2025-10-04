from modules.stt import listen_and_transcribe
from core.agent import run_agent
from modules.tts import speak

print("🎤 Speak something... Say 'end' to stop.")

while True:
    text = listen_and_transcribe()
    print("🎤 You said:", text)

    response = run_agent(text)
    print("🤖 Assistant:", response)

    # 🔊 Speak the response
    speak(response)

    if "END_PROGRAM" in response:
        print("🛑 Program ended.")
        break
