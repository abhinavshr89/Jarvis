from modules.stt import listen_and_transcribe
from core.agent import run_agent

def voice_mode():
    """Handle voice-based interaction"""
    print("🎤 Voice mode activated. Speak something... Say 'end' to stop.")
    while True:
        text = listen_and_transcribe()
        print("🎤 You said:", text)
        
        response = run_agent(text)
        print("🤖 Assistant:", response)
        
        if "END_PROGRAM" in response:
            print("🛑 Program ended.")
            break

def text_mode():
    """Handle text-based interaction"""
    print("⌨️  Text mode activated. Type your message... Type 'end' to stop.")
    while True:
        text = input("You: ").strip()
        if not text:
            continue
            
        response = run_agent(text)
        print("🤖 Assistant:", response)
        
        if "END_PROGRAM" in response or text.lower() == 'end':
            print("🛑 Program ended.")
            break

def main():
    """Main function with mode selection"""
    print("=" * 50)
    print("🤖 AI Assistant")
    print("=" * 50)
    print("\nChoose your input mode:")
    print("1. Voice mode (speech-to-text)")
    print("2. Text mode (keyboard input)")
    print("=" * 50)
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()

        if choice == "1":
            voice_mode()
            break
        elif choice == "2":
            text_mode()
            break
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
