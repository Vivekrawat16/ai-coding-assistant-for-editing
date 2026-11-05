#!/usr/bin/env python3
"""
Render Engine for YouTube Shorts / Reels
Composites 1080x1920 vertical layout with blurred dynamic background,
crisp centered 16:9 podcast video, 2-line hook banner, and kinetic ASS subtitles.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import config

def escape_drawtext(text: str) -> str:
    """Escapes text for FFmpeg drawtext filter."""
    return text.replace("'", "'\\\\\\''").replace(":", "\\:").replace(",", "\\,")

def render_podcast_short(
    input_buffer: str,
    slice_start: float,
    slice_duration: float,
    hook_line1: str,
    hook_line2: str,
    ass_subtitle_file: str,
    output_path: str
) -> bool:
    """
    Renders the final 1080x1920 Short.
    """
    print(f"🎬 Rendering Short: {output_path} (Duration: {slice_duration:.2f}s)...")

    if os.path.exists(output_path):
        os.remove(output_path)

    esc_h1 = escape_drawtext(hook_line1)
    esc_h2 = escape_drawtext(hook_line2)

    text_filters = (
        f"drawtext=text='{esc_h1}':font='{config.SUBTITLE_FONT}':fontsize=42:fontcolor=white:"
        f"box=1:boxcolor=black@0.75:boxborderw=14:x=(w-text_w)/2:y=420,"
        f"drawtext=text='{esc_h2}':font='{config.SUBTITLE_FONT}':fontsize=42:fontcolor=yellow:"
        f"box=1:boxcolor=black@0.75:boxborderw=14:x=(w-text_w)/2:y=486"
    )

    fade_start = max(0.0, slice_duration - 1.0)

    filter_complex = (
        f"[0:v]trim=start={slice_start}:duration={slice_duration},setpts=PTS-STARTPTS,"
        f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"gblur=sigma={config.BLUR_SIGMA},colorlevels=rimin=0.2:gimin=0.2:bimin=0.2[bg];"
        f"[0:v]trim=start={slice_start}:duration={slice_duration},setpts=PTS-STARTPTS,"
        f"scale=1080:608:force_original_aspect_ratio=increase,crop=1080:608,format=yuv420p[fg];"
        f"[bg][fg]overlay=0:656[comp1];"
        f"[comp1]{text_filters}[comp2];"
        f"[comp2]subtitles={ass_subtitle_file}[vfinal];"
        f"[0:a]atrim=start={slice_start}:duration={slice_duration},asetpts=PTS-STARTPTS,"
        f"afade=t=out:st={fade_start:.2f}:d=1.0[afinal]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", input_buffer,
        "-filter_complex", filter_complex,
        "-map", "[vfinal]",
        "-map", "[afinal]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", f"{slice_duration:.2f}",
        output_path
    ]

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"✅ Rendered successfully: {output_path} ({size_mb:.2f} MB)")
            return True
        else:
            print(f"❌ FFmpeg error: {res.stderr[-300:]}")
    except Exception as e:
        print(f"❌ Rendering execution error: {e}")

    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_buf = sys.argv[1]
        render_podcast_short(
            test_buf,
            5.70,
            14.46,
            "ANDREW TATE ON SUCCESS",
            "LISTEN TO THIS VERY CAREFULLY 🧠",
            "/tmp/test_captions.ass",
            "/tmp/test_rendered_tate.mp4"
        )
