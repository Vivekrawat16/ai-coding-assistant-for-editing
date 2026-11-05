#!/usr/bin/env python3
"""
Autonomous Podcast & Street Interview Clipping Pipeline
End-to-End Automation Runner:
1. Scans channel / search candidates
2. Finds exact heatmap peak replay second
3. Downloads 45s peak buffer (under 5MB)
4. Transcribes audio in ~1s using local faster-whisper
5. Finds tight 11.5s - 14.5s punchline climax & hook banner
6. Generates kinetic word-by-word highlighted ASS subtitles
7. Renders 1080x1920 vertical Short with blurred dynamic background
8. Saves to output/ directory and optionally uploads to Google Drive queue
"""

import os
import sys
import argparse
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import config
from source_scanner import discover_candidate, download_peak_buffer, mark_id_processed, extract_video_metadata, find_best_peaks
from slice_detector import transcribe_buffer, find_optimal_slice, generate_viral_hooks, generate_kinetic_ass
from render_short import render_podcast_short
from google_drive_uploader import upload_to_drive_queue
from youtube_uploader import upload_short

def run_pipeline(
    count: int = 1,
    custom_url: str = None,
    custom_search: str = None,
    upload_drive: bool = False,
    upload_youtube: bool = False,
    privacy_status: str = "public"
):
    print("=" * 65)
    print("🚀 STARTING PODCAST & STREET INTERVIEW CLIPPING PIPELINE")
    print(f"🎯 Target count: {count} Short(s)")
    print("=" * 65)

    completed = 0
    start_total = time.time()

    for idx in range(count):
        print(f"\n[{idx + 1}/{count}] Selecting candidate video...")
        
        target_url = None
        target_title = None
        peak_second = None
        video_id = None

        if custom_url:
            meta = extract_video_metadata(custom_url)
            if not meta:
                print(f"❌ Failed to extract metadata for {custom_url}")
                return
            target_url = custom_url
            target_title = meta.get("title", "Podcast Clip")
            video_id = meta.get("id")
            peaks = find_best_peaks(meta.get("heatmap") or [])
            peak_second = peaks[0]["start_time"] if peaks else (meta.get("duration", 100) * 0.4)
        elif custom_search:
            cand = discover_candidate(source_type="search", query_or_url=custom_search)
            if cand:
                target_url, target_title, peak_second, video_id = cand
        else:
            cand = discover_candidate(source_type="auto")
            if cand:
                target_url, target_title, peak_second, video_id = cand

        if not target_url:
            print("❌ No eligible unprocessed candidates found.")
            break

        print(f"📺 Selected: {target_title}")
        print(f"🔗 URL: {target_url} | Peak: {peak_second:.1f}s | ID: {video_id}")

        tmp_buffer = f"/tmp/buffer_{video_id}.mp4"
        tmp_ass = f"/tmp/captions_{video_id}.ass"
        out_short = str(config.OUTPUT_DIR / f"short_{video_id}_{int(peak_second)}.mp4")

        # Step 1: Download 45s buffer centered on peak
        success = download_peak_buffer(target_url, peak_second, tmp_buffer)
        if not success:
            print("❌ Failed to download buffer. Skipping...")
            continue

        # Step 2: Local Whisper Transcription
        words = transcribe_buffer(tmp_buffer)
        if not words:
            print("❌ Transcription returned 0 words. Skipping...")
            continue

        # Step 3: Find Optimal 11.5s - 14.5s Slice
        slice_start, slice_end, slice_text = find_optimal_slice(words, buffer_duration=45.0)
        slice_dur = slice_end - slice_start
        print(f"✂️ Sliced: {slice_start:.2f}s -> {slice_end:.2f}s ({slice_dur:.2f}s)")
        print(f"💬 Punchline: \"{slice_text}\"")

        # Step 4: Generate Hook Banners
        hook1, hook2 = generate_viral_hooks(target_title, slice_text)
        print(f"🏷️ Hook Line 1: {hook1}")
        print(f"🏷️ Hook Line 2: {hook2}")

        # Step 5: Generate Kinetic Subtitle File
        generate_kinetic_ass(words, slice_start, slice_end, tmp_ass)

        # Step 6: Render 1080x1920 Short
        rendered = render_podcast_short(
            input_buffer=tmp_buffer,
            slice_start=slice_start,
            slice_duration=slice_dur,
            hook_line1=hook1,
            hook_line2=hook2,
            ass_subtitle_file=tmp_ass,
            output_path=out_short
        )

        if rendered:
            completed += 1
            mark_id_processed(video_id)
            print(f"🎉 Short successfully saved: {out_short}")

            # Optional YouTube Shorts Upload
            if upload_youtube:
                yt_title = f"{hook1} | {hook2} #Shorts"
                yt_desc = f"{target_title}\n\nPunchline: \"{slice_text}\"\n\n#Shorts #Podcast #StreetInterview"
                upload_short(
                    video_path=out_short,
                    title=yt_title,
                    description=yt_desc,
                    privacy_status=privacy_status
                )

            # Optional Drive Queue Upload
            if upload_drive:
                upload_to_drive_queue(out_short)

        # Cleanup temporary files
        for p in [tmp_buffer, tmp_ass]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

    elapsed = time.time() - start_total
    print("\n" + "=" * 65)
    print(f"🏁 PIPELINE RUN COMPLETE! Generated {completed}/{count} Short(s) in {elapsed:.1f}s")
    print(f"📁 Output Directory: {config.OUTPUT_DIR}")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Podcast & Street Interview Clipping Pipeline")
    parser.add_argument("--count", type=int, default=1, help="Number of shorts to generate")
    parser.add_argument("--url", type=str, default=None, help="Specific YouTube URL to process")
    parser.add_argument("--search", type=str, default=None, help="Custom search query")
    parser.add_argument("--upload-drive", action="store_true", help="Upload rendered video to Google Drive queue")
    parser.add_argument("--upload-youtube", action="store_true", help="Upload rendered video to YouTube Shorts")
    parser.add_argument("--privacy", type=str, default="public", choices=["public", "unlisted", "private"], help="YouTube privacy status")

    args = parser.parse_args()
    run_pipeline(
        count=args.count,
        custom_url=args.url,
        custom_search=args.search,
        upload_drive=args.upload_drive,
        upload_youtube=args.upload_youtube,
        privacy_status=args.privacy
    )
