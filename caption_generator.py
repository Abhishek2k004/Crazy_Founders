from langdetect import detect
from openai import OpenAI
import json
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Languages supported
LANGUAGE_MAP = {
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam",
    "kn": "Kannada",
    "bn": "Bengali",
    "mr": "Marathi"
}

# Best posting times for Indian audiences
BEST_TIMES = {
    "Hindi": "6 PM – 9 PM",
    "Tamil": "7 PM – 10 PM",
    "Telugu": "6 PM – 10 PM",
    "Malayalam": "5 PM – 8 PM",
    "Kannada": "6 PM – 9 PM",
    "Bengali": "5 PM – 8 PM",
    "Marathi": "6 PM – 9 PM",
    "Indian-English": "6 PM – 9 PM"
}

def detect_language(text):
    """Detect language and return human-readable name."""
    try:
        lang_code = detect(text)
        return LANGUAGE_MAP.get(lang_code, "Indian-English")
    except:
        return "Indian-English"


def generate_caption_and_tags(clip_text, platform="Instagram"):
    """Generate Indian-style caption + hashtags in JSON format."""

    language = detect_language(clip_text)

    prompt = f"""
You are an expert Indian social media strategist.

Write a {platform} caption in an authentic **{language} tone**
for the following clip text:

\"\"\"{clip_text}\"\"\"

Guidelines:
- Caption should be short, viral-friendly, emotional/funny/motivational depending on text.
- Use local slang based on the language.
- Use Hinglish if Hindi.
- Use Tamil slang if Tamil.
- Hashtags should be trending in India (15–20 tags).
- No global hashtags like #motivation #funny #viral.
- Output *must* be JSON in this exact format:

{{
  "language": "{language}",
  "caption": "your caption here",
  "hashtags": ["#tag1", "#tag2", ...],
  "best_time": "{BEST_TIMES.get(language)}",
  "platform": "{platform}"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",     # you can change model here
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # FIXED LINE (no TypeError)
    return response.choices[0].message.content


# Local testing
if __name__ == "__main__":
    sample_text = "bhai ye galti mat karna, life me sabse badi mistake yahi hoti hai."
    print(generate_caption_and_tags(sample_text))
