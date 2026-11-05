#!/usr/bin/env python3
"""
Source Scanner & Heatmap Peak Extractor
Discovers high-engagement podcast / street interview videos,
extracts audience replay peaks, and downloads precise 45s buffers.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import config

def get_ytdlp_cmd() -> List[str]:
    venv_ytdlp = BASE_DIR / ".venv" / "bin" / "yt-dlp"
    if venv_ytdlp.exists():
        return [str(venv_ytdlp)]
    return ["yt-dlp"]

def load_processed_ids() -> List[str]:
    if config.PROCESSED_FILE.exists():
        try:
            with open(config.PROCESSED_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def mark_id_processed(video_id: str):
    ids = load_processed_ids()
    if video_id not in ids:
        ids.append(video_id)
        with open(config.PROCESSED_FILE, "w", encoding="utf-8") as f:
            json.dump(ids, f, indent=2)

def extract_video_metadata(youtube_url: str) -> Optional[Dict]:
    """Extract metadata including heatmap without downloading video."""
    cmd = get_ytdlp_cmd() + [
        "--dump-json",
        "--skip-download",
        "--no-playlist",
        youtube_url
    ]
    env = os.environ.copy()
    if "/home/vivek/.local/share/pnpm/bin" not in env.get("PATH", ""):
        env["PATH"] = f"/home/vivek/.local/share/pnpm/bin:{env.get('PATH', '')}"

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        if res.returncode == 0 and res.stdout.strip():
            return json.loads(res.stdout.strip().split("\n")[0])
    except Exception as e:
        print(f"❌ Error extracting metadata: {e}")
    return None

def find_best_peaks(heatmap: List[Dict], min_gap_seconds: float = 60.0, top_k: int = 3) -> List[Dict]:
    """Find local maxima replay peaks from heatmap data."""
    if not heatmap:
        return []

    # Sort heatmap points by replay value descending
    sorted_pts = sorted(heatmap, key=lambda x: x.get("value", 0), reverse=True)
    selected_peaks = []

    for pt in sorted_pts:
        start_time = pt.get("start_time", 0.0)
        # Check if far enough from existing selected peaks
        if all(abs(start_time - p["start_time"]) >= min_gap_seconds for p in selected_peaks):
            selected_peaks.append(pt)
            if len(selected_peaks) >= top_k:
                break

    return selected_peaks

def download_peak_buffer(youtube_url: str, peak_second: float, output_path: str, buffer_before: float = 15.0, buffer_after: float = 30.0) -> bool:
    """Download exact 45s buffer centered on the heatmap peak."""
    start_sec = max(0.0, peak_second - buffer_before)
    end_sec = peak_second + buffer_after
    section_str = f"*{int(start_sec)}-{int(end_sec)}"

    print(f"📥 Downloading 45s peak buffer [{int(start_sec)}s - {int(end_sec)}s] -> {output_path}...")
    
    cmd = get_ytdlp_cmd() + [
        "--download-sections", section_str,
        "--format", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
        "--output", output_path,
        "--force-overwrites",
        youtube_url
    ]

    env = os.environ.copy()
    if "/home/vivek/.local/share/pnpm/bin" not in env.get("PATH", ""):
        env["PATH"] = f"/home/vivek/.local/share/pnpm/bin:{env.get('PATH', '')}"

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        if res.returncode == 0 and os.path.exists(output_path):
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"✅ Buffer downloaded successfully ({size_mb:.2f} MB)")
            return True
        else:
            print(f"❌ yt-dlp error: {res.stderr[:200]}")
    except Exception as e:
        print(f"❌ Download failed: {e}")
    return False

def discover_candidate(source_type: str = "auto", query_or_url: Optional[str] = None) -> Optional[Tuple[str, str, float, str]]:
    """
    Finds next best candidate video and returns:
    (youtube_url, title, peak_second, video_id)
    """
    processed = set(load_processed_ids())

    targets = []
    if query_or_url:
        if "youtube.com" in query_or_url or "youtu.be" in query_or_url:
            targets.append({"name": "Custom URL", "type": "url", "url": query_or_url})
        else:
            targets.append({"name": "Custom Search", "type": "search", "query": query_or_url})
    else:
        targets = config.CURATED_SOURCES

    for src in targets:
        print(f"🔎 Scanning source: {src['name']}...")
        candidate_ids = []

        if src["type"] == "url":
            meta = extract_video_metadata(src["url"])
            if meta:
                vid = meta.get("id")
                heatmap = meta.get("heatmap") or []
                peaks = find_best_peaks(heatmap)
                peak_time = peaks[0]["start_time"] if peaks else (meta.get("duration", 60) * 0.4)
                return (src["url"], meta.get("title", "Podcast Moment"), peak_time, vid)
            continue

        search_target = src.get("query") or src.get("url")
        cmd = get_ytdlp_cmd() + [
            "--flat-playlist",
            "--playlist-end", "5",
            "--print", "%(id)s | %(title)s | %(view_count)s",
            search_target
        ]
        env = os.environ.copy()
        if "/home/vivek/.local/share/pnpm/bin" not in env.get("PATH", ""):
            env["PATH"] = f"/home/vivek/.local/share/pnpm/bin:{env.get('PATH', '')}"

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        if res.returncode != 0:
            continue

        for line in res.stdout.strip().split("\n"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                vid, title = parts[0], parts[1]
                if vid not in processed:
                    print(f"  👉 Found candidate: {title} (ID: {vid})")
                    full_url = f"https://www.youtube.com/watch?v={vid}"
                    meta = extract_video_metadata(full_url)
                    if not meta:
                        continue

                    heatmap = meta.get("heatmap") or []
                    peaks = find_best_peaks(heatmap)
                    if peaks:
                        peak_time = peaks[0]["start_time"]
                        print(f"  🔥 Found Heatmap Peak at {peak_time:.1f}s (Score: {peaks[0].get('value', 0):.2f})")
                        return (full_url, title, peak_time, vid)
                    else:
                        duration = meta.get("duration", 0)
                        if 60 < duration < 7200:
                            # Fallback: estimate mid-point climax
                            fallback_time = duration * 0.35
                            print(f"  ⚠️ No heatmap available. Using high-interest window at {fallback_time:.1f}s")
                            return (full_url, title, fallback_time, vid)

    return None

if __name__ == "__main__":
    cand = discover_candidate()
    if cand:
        url, title, peak, vid = cand
        print(f"Selected Candidate: {title}")
        print(f"URL: {url} | Peak: {peak}s | ID: {vid}")
