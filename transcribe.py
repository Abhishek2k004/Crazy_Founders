import whisper
import json
import os

AUDIO_FILE = "audio.wav"
TRANSCRIPT_FILE = "transcript.json"

def transcribe_audio():
    if not os.path.exists(AUDIO_FILE):
        print(f"❌ Audio file '{AUDIO_FILE}' not found. Run audio_extractor.py first.")
        return

    print("🧠 Loading Whisper model (small)...")
    model = whisper.load_model("small")  # later try: "medium" or "large"

    print("🎧 Transcribing audio... this may take some time.")
    result = model.transcribe(AUDIO_FILE)

    # Save full result (has language, segments, text, etc.)
    with open(TRANSCRIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ Transcript saved to: {TRANSCRIPT_FILE}")
    print("📝 Detected language:", result.get("language"))
    print("\nSample text:\n", result.get("text", "")[:300], "...\n")

if __name__ == "__main__":
    transcribe_audio()
