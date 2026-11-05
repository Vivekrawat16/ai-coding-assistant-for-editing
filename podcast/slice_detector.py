#!/usr/bin/env python3
"""
Slice Detector & Kinetic Caption Generator (Indian Content Optimized)
Uses local faster-whisper to analyze 45s audio buffers of Indian Podcasts & Street Interviews.
Finds punchline climax, generates catchy Hindi/Hinglish hook banners, and produces kinetic ASS subtitles.
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import config

def format_ass_time(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    cs = int(round((t - int(t)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

def transcribe_buffer(video_path: str) -> List[Dict]:
    """Transcribes audio using local faster-whisper base model (multilingual support)."""
    from faster_whisper import WhisperModel

    print(f"🎙️ Transcribing Indian content buffer: {video_path}...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    
    # Use task='translate' so Hindi/Hinglish audio gets clean, readable word-by-word kinetic subtitles
    segments, info = model.transcribe(video_path, task="translate", word_timestamps=True)

    words = []
    for s in segments:
        for w in s.words:
            w_text = w.word.strip().upper()
            if w_text:
                words.append({
                    "word": w_text,
                    "start": max(0.0, w.start),
                    "end": max(w.start + 0.1, w.end)
                })

    print(f"  📝 Transcribed {len(words)} words (Language: {info.language}).")
    return words

def find_optimal_slice(words: List[Dict], buffer_duration: float, target_duration: float = 12.8) -> Tuple[float, float, str]:
    """Finds the most coherent 11.5s - 14.5s window containing a complete thought."""
    if not words:
        mid = buffer_duration / 2.0
        start = max(0.0, mid - (target_duration / 2.0))
        return (start, start + target_duration, "VIRAL INDIAN MOMENT")

    center_time = buffer_duration / 2.0
    best_start = 0.0
    best_end = target_duration
    best_score = -9999.0

    for i, w in enumerate(words):
        w_start = w["start"]
        for j in range(i + 4, len(words)):
            w_end = words[j]["end"]
            dur = w_end - w_start
            if config.TARGET_MIN_DURATION <= dur <= config.TARGET_MAX_DURATION:
                center_dist = abs(((w_start + w_end) / 2.0) - center_time)
                ends_with_punch = words[j]["word"].endswith((".", "!", "?"))
                word_count = j - i + 1

                score = (word_count * 1.5) - (center_dist * 2.5) + (10.0 if ends_with_punch else 0.0)

                if score > best_score:
                    best_score = score
                    best_start = w_start
                    best_end = w_end

    if best_score == -9999.0:
        best_start = max(0.0, center_time - 6.5)
        best_end = min(buffer_duration, best_start + target_duration)

    slice_words = [w["word"] for w in words if best_start <= w["start"] <= best_end]
    full_slice_text = " ".join(slice_words)

    return (best_start, best_end, full_slice_text)

def generate_viral_hooks(title: str, slice_text: str) -> Tuple[str, str]:
    """Generates 2 high-curiosity hook banner lines customized for Indian content."""
    t_upper = title.upper()
    slice_upper = slice_text.upper()

    # Line 1: Creator / Show / Speaker
    if "OJHA" in t_upper:
        speaker = "AVADH OJHA SIR ON LIFE REALITY"
    elif "DIVYAKIRTI" in t_upper or "VIKAS" in t_upper:
        speaker = "DR VIKAS DIVYAKIRTI SIR"
    elif "RANVEER" in t_upper or "TRS" in t_upper or "BEERBICEPS" in t_upper:
        speaker = "THE RANVEER SHOW • TRS HINDI"
    elif "SHAMANI" in t_upper or "FIGURING OUT" in t_upper:
        speaker = "RAJ SHAMANI • FIGURING OUT"
    elif "PRAKHAR" in t_upper or "DOSTCAST" in t_upper:
        speaker = "PRAKHAR KE PRAVACHAN"
    elif "SHUBHANKAR" in t_upper:
        speaker = "SHUBHANKAR MISHRA UNPLUGGED"
    elif "REALHIT" in t_upper or "STREET" in t_upper or "COLLEGE" in t_upper or "DELHI" in t_upper:
        speaker = "INDIAN STREET INTERVIEW"
    elif "SAMAY" in t_upper or "LATENT" in t_upper:
        speaker = "SAMAY RAINA UNFILTERED"
    else:
        speaker = "HARSH INDIAN REALITY"

    # Line 2: The Provocative Punchline
    if "POWER" in slice_upper or "UTILITY" in slice_upper or "GAME" in slice_upper:
        line2 = "AGAR UTILITY KHATAM TOH GAME OVER 💀"
    elif "MONEY" in slice_upper or "PAISA" in slice_upper or "RICH" in slice_upper or "POVERTY" in slice_upper:
        line2 = "PAISA NAHI TOH LOG AUKAAT DIKHAYENGE 💸"
    elif "GIRL" in slice_upper or "WOMEN" in slice_upper or "DATING" in slice_upper or "LOVE" in slice_upper:
        line2 = "LADKI KA AISA JAWAB SUNKAR HOSH UD GAYE 😳"
    elif "PARENT" in slice_upper or "BAAP" in slice_upper or "FAMILY" in slice_upper:
        line2 = "BAAP SE PAISE MAANGNA BAND KARO 🚨"
    elif "SUCCESS" in slice_upper or "TARGET" in slice_upper or "LIFE" in slice_upper:
        line2 = "YE BAAT HAR YOUTH KO SAMAJHNI CHAHIYE 🧠"
    else:
        line2 = "SACH SUNOGE TOH RONGTE KHADE HO JAYENGE 🔥"

    return (speaker, line2)

def generate_kinetic_ass(
    words: List[Dict],
    slice_start: float,
    slice_end: float,
    output_ass_path: str,
    font_name: str = config.SUBTITLE_FONT
):
    """Generates an ASS subtitle file with 3-word chunks and glowing yellow active words."""
    trimmed_words = []
    for w in words:
        if w["start"] >= slice_start and w["end"] <= slice_end:
            trimmed_words.append({
                "word": w["word"],
                "start": max(0.0, w["start"] - slice_start),
                "end": max(0.1, w["end"] - slice_start)
            })

    chunks = []
    chunk_size = 3
    for i in range(0, len(trimmed_words), chunk_size):
        chunks.append(trimmed_words[i:i + chunk_size])

    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {config.VIDEO_WIDTH}",
        f"PlayResY: {config.VIDEO_HEIGHT}",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Kinetic,{font_name},{config.SUBTITLE_FONT_SIZE},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,0,2,30,30,520,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    for chunk in chunks:
        for active_idx, w in enumerate(chunk):
            st = format_ass_time(w["start"])
            et = format_ass_time(w["end"])

            text_parts = []
            for j, cw in enumerate(chunk):
                cleaned_word = re.sub(r"[^\w\s']", "", cw["word"]).upper()
                if j == active_idx:
                    # Active word in Glowing Yellow
                    text_parts.append(r"{\c&H0000FFFF&}" + cleaned_word + r"{\c&H00FFFFFF&}")
                else:
                    text_parts.append(cleaned_word)

            display_text = " ".join(text_parts)
            ass_lines.append(f"Dialogue: 0,{st},{et},Kinetic,,0,0,0,,{display_text}")

    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))

    print(f"  ✨ Kinetic ASS Subtitles generated: {output_ass_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        vid_path = sys.argv[1]
        words = transcribe_buffer(vid_path)
        start, end, text = find_optimal_slice(words, 40.0)
        h1, h2 = generate_viral_hooks("Avadh Ojha on Raj Shamani", text)
        print(f"Slice: {start:.2f}s -> {end:.2f}s ({end - start:.2f}s)")
        print(f"Hook: {h1} | {h2}")
        generate_kinetic_ass(words, start, end, "/tmp/test_indian_captions.ass")
