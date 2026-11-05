#!/usr/bin/env python3
"""
Configuration for Autonomous Indian Podcast & Street Interview Clipping Engine
Supports 1-minute (45s–58s) full-story Shorts and 15s punchline clips.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
PROCESSED_FILE = BASE_DIR / "processed_podcasts.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Top Indian Curated Sources
CURATED_SOURCES = [
    {
        "name": "Raj Shamani (Figuring Out)",
        "type": "search",
        "query": "ytsearch5:Raj Shamani podcast interview",
        "keywords": ["ojha", "vikas", "reality", "money", "power", "psychology", "dating", "dark", "truth"]
    },
    {
        "name": "The Ranveer Show (TRS Hindi)",
        "type": "search",
        "query": "ytsearch5:The Ranveer Show Hindi podcast",
        "keywords": ["secret", "mystery", "relationship", "truth", "ghost", "army", "god", "reality"]
    },
    {
        "name": "Prakhar ke Pravachan & Dostcast",
        "type": "search",
        "query": "ytsearch5:Prakhar ke Pravachan dating psychology podcast",
        "keywords": ["dating", "girls", "red flag", "breakup", "relationship", "psychology"]
    },
    {
        "name": "Shubhankar Mishra Unplugged",
        "type": "search",
        "query": "ytsearch5:Shubhankar Mishra podcast",
        "keywords": ["unplugged", "controversy", "truth", "bollywood", "cricket", "politics"]
    },
    {
        "name": "RealHit Indian Street Interviews",
        "type": "search",
        "query": "ytsearch5:RealHit street interview college",
        "keywords": ["dating", "college", "dogla", "girls", "salary", "relationship", "reality"]
    }
]

# Video Layout and Audio Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920

# Duration Settings: 48s - 58.5s for 1-minute full story YouTube Shorts
DEFAULT_MIN_DURATION = 45.0
DEFAULT_MAX_DURATION = 58.5

BLUR_SIGMA = 35

# Subtitle Settings
SUBTITLE_FONT = "DejaVu Sans"
SUBTITLE_FONT_SIZE = 58
ACTIVE_WORD_COLOR = "&H0000FFFF&"  # Bright Glowing Yellow
DEFAULT_WORD_COLOR = "&H00FFFFFF&" # Pure White

# Google Drive Queue (Optional sync to existing Drive queue)
GDRIVE_QUEUE_FOLDER_ID = (os.getenv("PODCAST_GDRIVE_FOLDER_ID") or os.getenv("PREME_GDRIVE_FOLDER_ID") or "").strip()
GDRIVE_SA_KEY = os.getenv("GDRIVE_SA_KEY", "")
