import os
import subprocess

VIDEO_FILE = "video.mp4"
AUDIO_FILE = "audio.wav"

def extract_audio():
    if not os.path.exists(VIDEO_FILE):
        print(f"❌ Video file '{VIDEO_FILE}' not found in current folder.")
        print("   Make sure 'video.mp4' is in the same folder as this script.")
        return

    cmd = [
        "ffmpeg",
        "-y",              # overwrite output if exists
        "-i", VIDEO_FILE,  # input video
        "-vn",             # no video
        AUDIO_FILE         # output audio
    ]

    print("🎥 Extracting audio from video...")
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"✅ Audio saved as: {AUDIO_FILE}")

if __name__ == "__main__":
    extract_audio()
