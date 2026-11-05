#!/usr/bin/env python3
"""
Configuration for Autonomous Street Interview & Podcast Clipping Engine
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
PROCESSED_FILE = BASE_DIR / "processed_podcasts.json"

# Create output dir if needed
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Target Channels & Search Queries for Street Interviews / Dating / Podcasts
CURATED_SOURCES = [
    {
        "name": "Bradley Martyn Raw Talk",
        "type": "search",
        "query": "ytsearch5:Bradley Martyn Raw Talk podcast",
        "keywords": ["destroyed", "tate", "dating", "gym", "sneako", "cheating", "relationship"]
    },
    {
        "name": "Whatever Podcast",
        "type": "channel",
        "url": "https://www.youtube.com/@whatever",
        "keywords": ["destroys", "debate", "dating", "average", "feminist", "single mom", "gold digger"]
    },
    {
        "name": "Sneako Debates & Street",
        "type": "search",
        "query": "ytsearch5:Sneako street debate podcast",
        "keywords": ["debate", "street", "interview", "girlfriend", "modern"]
    },
    {
        "name": "Fresh and Fit",
        "type": "search",
        "query": "ytsearch5:Fresh and Fit podcast debate",
        "keywords": ["debate", "girls", "dating", "accountability", "money"]
    }
]

# Video Layout and Audio Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
TARGET_MIN_DURATION = 11.5
TARGET_MAX_DURATION = 14.5
BLUR_SIGMA = 35

# Subtitle Settings
SUBTITLE_FONT = "DejaVu Sans"
SUBTITLE_FONT_SIZE = 58
ACTIVE_WORD_COLOR = "&H0000FFFF&"  # Bright Yellow (BGR ASS format)
DEFAULT_WORD_COLOR = "&H00FFFFFF&" # Pure White

# Google Drive Queue (Optional sync to existing Drive queue)
GDRIVE_QUEUE_FOLDER_ID = (os.getenv("PODCAST_GDRIVE_FOLDER_ID") or os.getenv("PREME_GDRIVE_FOLDER_ID") or "").strip()
GDRIVE_SA_KEY = os.getenv("GDRIVE_SA_KEY", "")
