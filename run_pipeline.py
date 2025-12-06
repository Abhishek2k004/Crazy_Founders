import os
import json
import subprocess

from reel_selector import get_best_clips
from caption_generator import generate_caption_and_tags
from subtitles import create_srt_for_clip, burn_subtitles


VIDEO_FILE = "video.mp4"
TRANSCRIPT_FILE = "transcript.json"
CLIPS_DIR = "clips"
OUTPUT_DIR = "final_output"


# ---------------------------------------------------------
# Cut a video clip using ffmpeg (fast, no re-encoding)
# ---------------------------------------------------------
def cut_clip(input_video, start, end, output_path):
    duration = end - start
    cmd = [
        "ffmpeg",
        "-y",
        "-ss", str(start),
        "-i", input_video,
        "-t", str(duration),
        "-c", "copy",
        output_path
    ]
    print("✂️ Cutting clip:", " ".join(cmd))
    subprocess.run(cmd, check=True)


# ---------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------
def main():
    # --------------------------
    # Check input files
    # --------------------------
    if not os.path.exists(TRANSCRIPT_FILE):
        print(f"❌ {TRANSCRIPT_FILE} not found. Run transcribe.py first.")
        return

    if not os.path.exists(VIDEO_FILE):
        print(f"❌ {VIDEO_FILE} not found. Place video.mp4 in this folder.")
        return

    # --------------------------
    # Step 1: Get best reel-worthy clips
    # --------------------------
    print("\n🔍 Finding reel-worthy clips (AI + Indian slang ranking)...\n")
    clips = get_best_clips(TRANSCRIPT_FILE, top_k=5)

    if not clips:
        print("❌ No clips detected.")
        return

    for i, c in enumerate(clips, start=1):
        print("-" * 60)
        print(f"🎬 Clip #{i}")
        print(f"Start : {c['start']} sec")
        print(f"End   : {c['end']} sec")
        print(f"Score : {c['score']}")
        print(f"Text  : {c['text'][:180]}...")

    # --------------------------
    # Prepare folders
    # --------------------------
    os.makedirs(CLIPS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --------------------------
    # Step 2: Generate clips
    # --------------------------
    print("\n🚀 Generating video clips...\n")

    for i, c in enumerate(clips, start=1):
        out_clip = os.path.join(CLIPS_DIR, f"clip_{i}.mp4")
        cut_clip(VIDEO_FILE, c["start"], c["end"], out_clip)
        c["clip_path"] = out_clip

    # --------------------------
    # Step 3: Subtitles (SRT + burned-in)
    # --------------------------
    print("\n🔤 Creating subtitles...\n")

    for i, c in enumerate(clips, start=1):
        srt_path = os.path.join(OUTPUT_DIR, f"clip_{i}.srt")
        create_srt_for_clip(TRANSCRIPT_FILE, c["start"], c["end"], srt_path)
        c["srt_path"] = srt_path

        burned_path = os.path.join(OUTPUT_DIR, f"clip_{i}_subtitled.mp4")
        burn_subtitles(c["clip_path"], srt_path, burned_path)
        c["final_subtitled"] = burned_path

        print(f"✅ Subtitles ready → {burned_path}")

    # --------------------------
    # Step 4: Generate Captions + Hashtags (Indian Engine)
    # --------------------------
    print("\n📝 Generating captions + hashtags for each clip...\n")

    for i, c in enumerate(clips, start=1):
        print(f"🧠 AI Captioning Clip #{i}...\n")

        text_for_caption = c["text"]
        caption_json = generate_caption_and_tags(text_for_caption, platform="Instagram")

        # Decode JSON from AI
        try:
            caption_data = json.loads(caption_json)
        except:
            caption_data = {"raw_output": caption_json}

        c["caption_data"] = caption_data

        print(f"✨ Caption Generated:\n{json.dumps(caption_data, indent=2, ensure_ascii=False)}\n")

    # --------------------------
    # Step 5: Save the final summary
    # --------------------------
    result_file = os.path.join(OUTPUT_DIR, "results.json")
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(clips, f, indent=2, ensure_ascii=False)

    print("\n🎉 ALL DONE!")
    print(f"📁 Final output saved in folder: {OUTPUT_DIR}")
    print(f"📄 Summary JSON: {result_file}")
    print("🎬 Check the final clips, subtitles, and captions!\n")


if __name__ == "__main__":
    main()
