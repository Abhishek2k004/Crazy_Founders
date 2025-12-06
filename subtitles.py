import json
import subprocess
import os


def create_srt_for_clip(transcript_file, start_time, end_time, output_path):
    """
    Create an SRT for only the transcript lines between start_time and end_time.
    """

    with open(transcript_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    if not segments:
        print("❌ No segments found in transcript.json")
        return

    selected_segments = [
        seg for seg in segments
        if seg["end"] >= start_time and seg["start"] <= end_time
    ]

    if not selected_segments:
        print(f"⚠ No transcript overlap found for clip window {start_time}–{end_time}")
        return

    def ts(t):
        ms = int((t % 1) * 1000)
        t = int(t)
        s = t % 60
        m = (t // 60) % 60
        h = t // 3600
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    lines = []
    index = 1

    for seg in selected_segments:
        seg_start = max(seg["start"], start_time)
        seg_end = min(seg["end"], end_time)

        lines.append(str(index))
        lines.append(f"{ts(seg_start)} --> {ts(seg_end)}")
        lines.append(seg["text"].strip())
        lines.append("")
        index += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ SRT created: {output_path}")


def detect_resolution(video_path):
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "json",
            video_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        w = data["streams"][0]["width"]
        h = data["streams"][0]["height"]
        return w, h
    except:
        print("⚠ Resolution detection failed, using default 1280x720")
        return 1280, 720


def burn_subtitles(input_video, srt_file, output_video):
    if not os.path.exists(srt_file):
        print(f"❌ SRT file not found: {srt_file}")
        return

    w, h = detect_resolution(input_video)
    print(f"📐 Video resolution: {w} x {h}")

    OUT_W, OUT_H = 1080, 1920

    vf_filter = (
        "scale=-2:1920:force_original_aspect_ratio=decrease,"
        f"pad={OUT_W}:{OUT_H}:(ow-iw)/2:(oh-ih)/2,"
        f"subtitles='{srt_file}':force_style='"
        "FontName=Arial,FontSize=36,Alignment=2,"
        "OutlineColour=&H66000000,BorderStyle=3'"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_video,
        "-vf", vf_filter,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "128k",
        output_video,
    ]

    print("\n🔥 Running FFmpeg:\n", " ".join(cmd), "\n")
    subprocess.run(cmd, check=True)
    print(f"🎉 Subtitles burned → {output_video}")
