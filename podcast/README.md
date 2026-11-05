# 🎙️ Autonomous Street Interview & Podcast Clipping Engine

A local, high-retention clipping engine that automatically finds viral climax moments from podcast and street interview videos, downloads precise 45-second peak buffers, slices the tight 12–14s punchline, generates kinetic glowing captions, and renders 1080x1920 vertical Shorts for YouTube & Instagram.

---

## ⚡ How It Works (Zero Guesswork & Zero API Fees)

1. **Source Discovery**: Monitors top channels (Bradley Martyn, Whatever, Sneako, Fresh & Fit).
2. **Heatmap Peak Detection**: Queries YouTube's internal 100-point audience replay graph (`heatmap`) to find the exact global replay peak.
3. **45s Peak Buffer**: Downloads only a 45-second window around that climax (under 5 MB) without downloading full 2-hour videos.
4. **Local Transcription**: Uses `faster-whisper` (`tiny.en`, int8 quantization) to transcribe speech with word-level timestamps in ~1.0 second on CPU.
5. **Punchline Slicer**: Mathematically isolates the tightest 11.5s–14.5s sentence/dialogue sequence around the peak.
6. **Hook Generator**: Creates high-curiosity 2-line hook banners.
7. **Kinetic Caption Generator**: Generates ASS subtitles with 3-word chunks and glowing yellow active words (`&H0000FFFF&`).
8. **FFmpeg Compositor**: Renders a vertical 1080x1920 Short with blurred dynamic background, crisp centered 16:9 podcast video, hook banner, and burned kinetic subtitles in ~15 seconds.

---

## 🚀 Quick Usage

### 1. Auto-discover and generate next viral Short:
```bash
/home/vivek/podcast_clipping/.venv/bin/python pipeline.py --count 1
```

### 2. Process a specific YouTube podcast / interview:
```bash
/home/vivek/podcast_clipping/.venv/bin/python pipeline.py --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

### 3. Search and clip a specific topic/guest:
```bash
/home/vivek/podcast_clipping/.venv/bin/python pipeline.py --search "Sneako street debate"
```

### 4. Upload finished Shorts directly to Google Drive queue:
```bash
/home/vivek/podcast_clipping/.venv/bin/python pipeline.py --count 3 --upload-drive
```

---

## 📁 Project Structure

```
podcast_clipping/
├── config.py                 # Channel sources, font, and resolution settings
├── source_scanner.py         # Heatmap extractor & 45s buffer downloader
├── slice_detector.py         # Local faster-whisper transcription & punchline selector
├── render_short.py           # 1080x1920 compositor with kinetic captions
├── google_drive_uploader.py  # Google Drive queue uploader (Service Account & CLI)
├── pipeline.py               # Main CLI orchestrator
├── processed_podcasts.json   # Video deduplication ledger
└── output/                   # Ready-to-post 1080x1920 vertical Shorts (.mp4)
```
