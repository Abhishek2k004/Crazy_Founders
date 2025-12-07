🚀 Crazy Founders – AI Reel Generator
Cut, caption & convert long videos into Instagram-ready reels — automatically.
<p align="center"> <img src="https://raw.githubusercontent.com/Abhishek2k004/Crazy_Founders/5ef67092f86a1a5cade9366b004e4324e34b80c4/banner.jpg" width="900"> </p>
🎯 Overview

Crazy Founders – AI Reel Generator is a fully automated system that transforms long-form videos into short, Instagram-optimized reels.

The pipeline:

✔ Extracts audio
✔ Transcribes using Whisper
✔ Detects viral hooks (Indian slang-aware)
✔ Cuts clips with FFmpeg
✔ Generates SRT subtitles
✔ Burns subtitles into portrait reels
✔ Generates captions + regional hashtags
✔ Outputs polished Instagram-ready reels

Built for creators, founders, YouTubers, podcast teams, and content agencies.

✨ Key Features

🎬 Intelligent Clip Detection (India-focused)
Detects Indian hook-phrases like:
“sun na”
“vinandi”
“shono”
“bhau”
Ranks emotional, humorous, or high-engagement moments.
Skips filler content.

🧠 AI Caption Generator
Generates platform-optimized captions
Adds trending regional hashtags (Hindi, Tamil, Telugu, Bengali, Kannada…)
Provides reel-style punchlines

📝 Auto Subtitles
Creates SRT from transcript
Burned subtitles include:
Bold white captions
Black outline
Center/bottom safe-zone alignment

📱 Instagram Reel Formatting (1080×1920)
Converts landscape → portrait
Adds clean padding
Ensures safe-area captions
🚀 Fully Automated Pipeline

Run everything with:
python run_pipeline.py
Output is saved to:
final_output/

📁 Project Structure
Crazy_Founders/
│
├── caption_generator.py      # AI captions + hashtags
├── reel_selector.py          # Indian slang scoring
├── subtitles.py              # SRT creation + burning
├── audio_extractor.py        # Extract audio
├── transcribe.py             # Whisper transcription
├── run_pipeline.py           # Full automation
│
├── video.mp4                 # Input video
├── transcript.json           # Whisper output
├── clips/                    # Auto clips
└── final_output/             # Final reels

⚙️ Installation Guide
1️⃣ Clone the repo
git clone https://github.com/Abhishek2k004/Crazy_Founders.git
cd Crazy_Founders

2️⃣ Create virtual environment
python -m venv env
env\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

🔑 Environment Variables
Create .env file:
OPENAI_API_KEY=your_key_here


⚠️ Never commit this file.

▶️ Run the Pipeline
Place your input file:
video.mp4


Start processing:
python run_pipeline.py

📂 Output Example
final_output/
│
├── clip_1.mp4
├── clip_1.srt
├── clip_1_subtitled.mp4
├── clip_1_caption.json
├── clip_2_subtitled.mp4
└── ...

🤝 Contributing (Team Workflow)
git checkout -b feature-name
git add .
git commit -m "Added feature-name"
git push origin feature-name


Then open a Pull Request.

🧪 Upcoming Features
🎵 Auto background music
✨ Subtitle animations
🎚️ Reframe + zoom-cuts
🧩 AI scene segmentation
☁️ FastAPI backend

🖥️ Web dashboard

👨‍💻 Built with ❤️ by Crazy Founders Team

Focused on India-first AI video automation.
