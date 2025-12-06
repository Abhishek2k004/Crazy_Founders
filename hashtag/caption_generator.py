from langdetect import detect
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEYsk-proj-dj0T6lqfjk_LLueytWXUxWvkgKN4DlA4WZosys1K2xycV-lPEYFlY5-4H-UNe7Q2hM5-Oq7gLTT3BlbkFJhHFj6HWka7pjcycbTKycrUG9IZ4uXWz90AIDOXM2sGqbAEHMK3UTGsvIEbxwCgy6b47b4UbV4A")

# Recommended: build local keyword sets for tones in future
LANGUAGE_LABELS = {
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam",
    "kn": "Kannada",
    "bn": "Bengali",
    "mr": "Marathi"
}

# Platform posting time recommendations (sample)
BEST_TIMES = {
    "Hindi": "6 PM – 9 PM",
    "Tamil": "7 PM – 10 PM",
    "Telugu": "6 PM – 10 PM",
    "Malayalam": "5 PM – 8 PM",
    "Kannada": "6 PM – 9 PM",
    "Bengali": "5 PM – 8 PM",
    "Marathi": "6 PM – 9 PM"
}


def detect_language(text):
    try:
        lang = detect(text)
        return LANGUAGE_LABELS.get(lang, "Indian-English")
    except:
        return "Indian-English"


def generate_caption(text, platform="Instagram"):
    lang = detect_language(text)

    prompt = f"""
You are an expert Indian social media copywriter.

Generate a reel caption + 15 hashtags in an authentic **{lang} Indian tone**
based on this clip:

Clip text:
\"\"\"{text}\"\"\"

Rules:
- Keep captions short (one line)
- Keep tone local, natural, and culturally accurate
- Use Hinglish if Hindi audience
- Use Tamil slang if Tamil audience
- Use Telugu slang if Telugu audience
- Hashtags must be trending in India
- Do NOT use generic global hashtags (#motivation #funny)
- Always give BEST posting time for {lang} audience

Output must be JSON:

{{
 "language": "{lang}",
 "caption": "...",
 "hashtags": ["#tag1", "#tag2", ...],
 "best_time": "{BEST_TIMES.get(lang, '6 PM – 9 PM')}"
}}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]


if __name__ == "__main__":
    sample_clip = "bhai ye galti mat karna, life me sabse badi mistake yehi hoti hai."
    print(generate_caption(sample_clip))
