<p align="center"> <img src="https://raw.githubusercontent.com/Abhishek2k004/Crazy_Founders/main/banner.png" width="90%" /> </p>


🎯 Overview

Crazy Founders – AI Reel Generator is an end-to-end automated pipeline that:

✔ Extracts audio
✔ Generates transcript using Whisper
✔ Identifies viral moments using Indian slang + hook scoring
✔ Cuts clips with FFmpeg
✔ Creates SRT subtitles
✔ Auto-burns subtitles in portrait reel format
✔ Generates Indian-style captions & hashtags using AI
✔ Outputs Instagram-ready reels

This tool is built for content creators, founders, podcast teams, and agencies.

✨ Features
🎬 Intelligent Clip Detection (India-focused)

Detects hooks like “sun na”, “vinandi”, “shono”, “bhau”

Scores emotional, humorous, or high-engagement moments

Filters intro or filler content

🧠 AI Caption Generator

Generates platform-optimized captions

Produces regional hashtags (Hindi, Tamil, Telugu, Bengali, Kannada…)

Includes trending-style lines

📝 Auto Subtitles

SRT creation from transcript

Burned subtitles with:

Bold white text

Black outline

Center/Bottom alignment

📱 Auto Portrait Reel Formatting

Converts horizontal → portrait (1080×1920)

Adds clean padding

Ensures Instagram safe-area layout

🚀 Fully Automated Pipeline

Just run:

python run_pipeline.py


And it outputs everything into final_output/.

🗂️ Project Structure
Crazy_Founders/
│
├── caption_generator.py      # AI captions + hashtags
├── reel_selector.py          # Indian slang-based clip scoring
├── subtitles.py              # SRT generation + burned captions
├── audio_extractor.py        # Extract audio from MP4
├── transcribe.py             # Whisper transcript generator
├── run_pipeline.py           # Full automation
│
├── video.mp4                 # Input video (you provide)
├── transcript.json           # Whisper output
├── clips/                    # Auto-generated clips
└── final_output/             # Final reels + SRTs

⚙️ Installation
1️⃣ Clone repo
git clone https://github.com/Abhishek2k004/Crazy_Founders.git
cd Crazy_Founders

2️⃣ Create virtual environment
python -m venv env
env\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

🔑 Environment Variable Setup

Create .env file:

OPENAI_API_KEY=your_key_here


Never commit this file.

▶️ How to Run the Full Pipeline

Place your input video:

video.mp4


Then run:

python run_pipeline.py


Pipeline steps:

Extract audio

Generate transcript

Score and find best reel-worthy clips

Cut video using FFmpeg

Create subtitles (SRT)

Burn subtitles into final video

Generate captions + hashtags

Save everything under final_output/

📂 Output Example
final_output/
│
├── clip_1.mp4
├── clip_1.srt
├── clip_1_subtitled.mp4
├── clip_1_caption.json
│
├── clip_2.mp4
├── clip_2_subtitled.mp4
└── ...

📸 Screenshots (Add Later)
![Workflow](https://via.placeholder.com/1000x500.png?text=Pipeline+Workflow)
![Output Example](https://via.placeholder.com/600x800.png?text=Reel+Output+Preview)

🤝 Contributing (For Your Team)

Clone repo

Create a new branch:

git checkout -b feature-xyz


Work on your feature

Commit changes:

git add .
git commit -m "Added feature XYZ"


Push your branch:

git push origin feature-xyz


Create a Pull Request (PR) on GitHub

🧪 Upcoming Features (Roadmap)

🎵 Auto background music insertion

🎨 Dynamic subtitle animations

🎚️ Reframing + zoom cuts

🧩 AI scene detection

☁️ Cloud deployment (FastAPI backend)

📝 Web UI dashboard

🧑‍💻 Built by

Crazy Founders Team
For India-first AI video automation
