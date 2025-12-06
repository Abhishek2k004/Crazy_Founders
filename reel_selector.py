import json

# ---------------------------------------------------------
# 🔥 MULTILINGUAL VIRAL HOOK PHRASES (high-impact openers)
# ---------------------------------------------------------

HOOK_PHRASES = [
    # Hindi / Hinglish
    "sun na", "ek baat bataun", "sun bhai", "dekho yaar", "bata raha hoon",
    "ye galti mat karna", "sabse badi mistake", "truth about life",
    "ek baat yaad rakhna", "ye baat life me zaroor sunna",
    "meri baat dhyaan se sunna", "aaj main tumhe ek baat bataunga",
    "jo main bolne wala hoon", "iska effect zindagi bhar rahega",

    # Tamil
    "listen pannunga", "solren da", "paathu da", "idhu kandippa venum",
    "oru vishayam sonna", "ketkunga", "idhu ungalukku romba mukhyam",

    # Telugu
    "vinandi", "cheppanu kada", "okkasari vinnu", "idi chala important",
    "oka matalu vinnara", "idi mee life ni marchestundi",

    # Malayalam
    "kelkka", "oru karyam parayam", "idhu nalla ariyenda",
    "oru important vishayam parayatte",

    # Kannada
    "kelri", "ondhu vishaya helteeni", "idu tumba mukhya",
    "idu neevu khanditha kelbeku",

    # Bengali
    "shono", "ekta kotha boli", "eta khub important",
    "amar kotha mon diye shono",

    # Marathi
    "eka goshta sangto", "aiku naka", "ha point lakshat theva",
    "he tumcha life badlu shakto",
]


# ---------------------------------------------------------
# 🔥 INDIAN SLANG (high engagement / high energy)
# ---------------------------------------------------------

DESI_SLANG = [
    # Generic Indian
    "bhai", "yaar", "bro", "mast", "jugaad", "scene", "level", "solid",
    "timepass", "full power", "jhakas", "kadak", "toofani",

    # Tamil slang
    "da", "dei", "machan", "vera level", "massu", "semma", "rowdy",

    # Telugu slang
    "ra", "anna", "bhayya", "baagunde", "mass ga undhi", "dhamki",

    # Malayalam slang
    "polichu", "mone", "molu", "mass aanu", "kenz",

    # Kannada slang
    "maga", "guru", "super ri", "bombaat", "saaku",

    # Bengali slang
    "baapok", "fatafati", "pagol", "dosto", "heavy",

    # Marathi slang
    "bhau", "jhakkas", "mastach", "zyada", "khatarnaak",
]


# ---------------------------------------------------------
# 🔥 HUMOR / COMEDY / ROAST DETECTION
# ---------------------------------------------------------

HUMOR_WORDS = [
    # Hinglish
    "funny", "meme", "comedy", "lol", "bezzati", "roast",
    "ye dekh", "bawaal", "toofan", "majak", "faltu",

    # Tamil
    "nakkal", "kalai", "jollya", "sarakku joke",

    # Telugu
    "navvu", "pichodu", "jokega undhi", "hilarious",

    # Bengali
    "haste haste", "moja", "hasir dose", "obhakto",

    # Marathi
    "vinodi", "mazaak", "jhakkas comedy",
]


# ---------------------------------------------------------
# 🔥 VALUE / KNOWLEDGE / MOTIVATION TERMS
# ---------------------------------------------------------

VALUE_WORDS = [
    "secret", "truth", "strategy", "plan", "tips", "skill",
    "career", "money", "paisa", "success", "growth", "mindset",
    "focus", "hardwork", "dedication", "improvement",

    # Hindi
    "safalta", "rahasya", "kaushal", "seekh", "mehnat",

    # Tamil
    "vetri", "thagaval", "arivu", "payan",

    # Telugu
    "nijam", "samacharam", "vijayam", "sadhinchadam",

    # Malayalam
    "vijayam", "ariyam", "lesson", "padikkanam",

    # Marathi
    "yash", "upay", "salah", "mahatvapurn",
]


# ---------------------------------------------------------
# ❌ INTRO PHRASES (low value for reel hooks)
# ---------------------------------------------------------

INTRO_PHRASES = [
    "welcome back", "subscribe", "like share", "mera naam",
    "is video mein", "aaj hum baat", "channel ko subscribe",
    "smash the like button", "follow for more",
    "intro", "today we will talk about",
]


# ---------------------------------------------------------
# Helper: count how many patterns appear in text
# ---------------------------------------------------------

def count_matches(text, patterns):
    text = text.lower()
    return sum(1 for p in patterns if p in text)


# ---------------------------------------------------------
# Sliding window generator:
# creates 25s windows sliding every 10s
# ---------------------------------------------------------

def create_windows(segments, window_size=25.0, step_size=10.0):
    """
    Turn small whisper segments into fixed-length windows.
    Each window is a candidate reel clip.

    segments: list of {start, end, text}
    window_size: length of each clip in seconds
    step_size: how much to slide the window in seconds
    """
    if not segments:
        return []

    windows = []
    t = segments[0]["start"]
    end_time = segments[-1]["end"]

    while t + window_size <= end_time:
        text_parts = []

        for seg in segments:
            if seg["end"] < t:
                continue
            if seg["start"] > t + window_size:
                break
            text_parts.append(seg["text"].strip())

        if text_parts:
            windows.append({
                "start": round(t, 2),
                "end": round(t + window_size, 2),
                "text": " ".join(text_parts)
            })

        t += step_size

    return windows


# ---------------------------------------------------------
# FINAL SCORING: MULTILINGUAL, VIRAL-ORIENTED
# ---------------------------------------------------------

def score_window(w):
    """
    Assign a score to a window based on:
    - hooks
    - slang
    - humor
    - value
    - intro penalty
    - word-count sweet spot
    """
    text = w["text"].lower()
    score = 0.0

    # strong hooks = 3 pts each
    score += count_matches(text, HOOK_PHRASES) * 3.0

    # desi slang = 2 pts each
    score += count_matches(text, DESI_SLANG) * 2.0

    # humor/comedy = 2.5 pts each
    score += count_matches(text, HUMOR_WORDS) * 2.5

    # value/motivation/knowledge = 2 pts each
    score += count_matches(text, VALUE_WORDS) * 2.0

    # intros = -3 pts each
    score -= count_matches(text, INTRO_PHRASES) * 3.0

    # Ideal word count range (not too short, not too long)
    wc = len(text.split())
    if 15 <= wc <= 60:
        score += 2.0

    return score


# ---------------------------------------------------------
# MAIN: get_best_clips -> used by run_pipeline.py
# ---------------------------------------------------------

def get_best_clips(transcript_file: str, top_k: int = 5):
    """
    Read transcript.json, generate candidate windows,
    score them, and return the top_k best clip candidates.
    Each result has: start, end, text, score.
    """
    with open(transcript_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    if not segments:
        print("❌ No segments found in transcript.json")
        return []

    windows = create_windows(segments)

    scored = []
    for w in windows:
        scored.append({
            **w,
            "score": score_window(w)
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
