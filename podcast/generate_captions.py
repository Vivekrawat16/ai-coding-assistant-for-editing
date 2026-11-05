#!/usr/bin/env python3
"""
Kinetic Word-by-Word Caption Generator
Generates ASS subtitle file with yellow glowing highlighted words for TikTok/Shorts.
"""

from faster_whisper import WhisperModel

def format_ass_time(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    cs = int(round((t - int(t)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

def generate_kinetic_ass(video_mp4: str, output_ass: str, font_name: str = "DejaVu Sans"):
    print(f"Loading Whisper model and transcribing {video_mp4}...")
    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(video_mp4, word_timestamps=True)

    words = []
    for s in segments:
        for w in s.words:
            w_text = w.word.strip().upper()
            if w_text:
                words.append({"word": w_text, "start": max(0.0, w.start), "end": max(w.start + 0.1, w.end)})

    print(f"Detected {len(words)} words.")

    chunks = []
    chunk_size = 3
    for i in range(0, len(words), chunk_size):
        chunks.append(words[i:i + chunk_size])

    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{font_name},58,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,0,2,30,30,520,1",
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
                word_str = cw["word"]
                if j == active_idx:
                    # Active word in Bright Yellow with bold pop
                    text_parts.append(r"{\c&H0000FFFF&}" + word_str + r"{\c&H00FFFFFF&}")
                else:
                    text_parts.append(word_str)

            display_text = " ".join(text_parts)
            ass_lines.append(f"Dialogue: 0,{st},{et},Default,,0,0,0,,{display_text}")

    with open(output_ass, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))

    print(f"✅ Kinetic ASS subtitle file generated: {output_ass}")

if __name__ == "__main__":
    generate_kinetic_ass("/tmp/interview_trimmed_12s.mp4", "/tmp/interview_captions.ass")
