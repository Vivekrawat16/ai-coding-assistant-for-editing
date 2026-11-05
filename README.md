# 🎬 AI Coding Assistant for Video Editing & Automations

> Central repository preserving the **Rules, Memories, FFmpeg Compositing Patterns, and Automated Pipelines** for AI Coding Assistants (Antigravity, Cursor, Claude Code, GitHub Copilot).

---

## 🏗️ Dual Track Architecture

This repository strictly separates two independent video production and social media automation engines:

```
ai-coding-assistant-for-editing/
├── .cursorrules                       # AI assistant context & direct rules
├── AGENTS.md                          # Multi-agent persistent memory
├── RULES.md                           # Master rulebook (ratios, durations, constraints)
├── requirements.txt                   # Universal dependencies
│
├── personal/                          # 🟢 TRACK 1: PERSONAL (Reddit Memes)
│   ├── audit/                         # Performance auditing for personal meme page
│   │   └── performance_auditor.py
│   ├── generator/                     # 2-Day Topic Clustering Feedback Loop
│   │   ├── cluster_generator.py
│   │   └── cluster_pipeline.py
│   ├── renderer/                      # Option A Centered Dark Renderer
│   │   └── render_centered_meme.py
│   └── assets/                        # Fonts & Core Character Raw Clips
│       ├── Montserrat-Bold.ttf
│       └── clips/                     # Akshay, Paresh, Baburao, Rajpal, Nana, Cillian
│
├── client/                            # 🔵 TRACK 2: CLIENT CLIPPING (Streamer Preme)
│   ├── fetcher/                       # Twitch / Kick clip scraper (yt-dlp)
│   │   └── fetch_clips.py
│   ├── hooks/                         # 2-line viral hook & caption generator
│   │   └── hook_engine.py
│   ├── renderer/                      # 1080x1920 with blurred background & Preme overlay
│   │   └── render_engine.py
│   ├── pipeline.py                    # End-to-end Preme ingest -> render -> drive queue
│   ├── poster.py                      # Post to Client Account & log to Desktop
│   └── assets/
│       └── Preme_Overlay.png          # Official campaign branding
│
├── shared/                            # 🟡 SHARED UTILITIES
│   ├── cloud_post_reel.py             # Serverless Google Drive -> Instagram uploader
│   └── gdrive_uploader.py             # Resilient Google Drive API / CLI uploader
│
└── .github/workflows/                 # ☁️ 24/7 GITHUB ACTIONS CLOUD RUNNERS
    ├── personal_meme_cluster_loop.yml # Runs every 2 days (1:30 PM IST)
    ├── personal_post_reel.yml         # 5x daily meme post (10AM, 2PM, 5PM, 8PM, 11PM)
    ├── client_preme_daily_pipeline.yml# Daily Preme clipping at 10:30 AM IST
    └── client_post_preme_reel.yml     # Preme posting every 3 hours
```

---

## ⚡ Quick Comparison: Personal vs Client

| Feature | Track 1: Personal Memes | Track 2: Client Clipping |
| :--- | :--- | :--- |
| **Account** | Personal Meme Account | Client Campaign Account |
| **Theme** | Relatable Desi/Pop-culture Memes | Twitch / Kick Streamer Highlights |
| **Format** | Option A (Pure Black Canvas) | Blurred BG + 16:9 Stream Center |
| **Duration** | **6.0 – 8.0s** | **10.0 – 15.0s** (Strict 15s max) |
| **Branding** | Customizable subtle watermark | Official `Preme_Overlay.png` badge |
| **Campaign Goal** | Organic Meme Growth & Virality | **$50 / 100K Views Bounty** on clipping.net |
| **Drive Queue** | `15tEG1buRhHi8g4lkv98KMJC_-LHupuvV` | `1NuU7Jc3zLVnd08UZh6U-2QrlWxOmEWXr` |
| **Drive Archive** | `19oTHwlAxucPomUfLXAOanyDyzTMeshya` | `1E3xbmMxuMykWskFagbQ155mn5Dq1QWfG` |

---

## 🚫 Hard Execution Rules for AI Assistants

1. **Reel Feed Upload ONLY**: Never post to Stories (`cl.media_share_to_story` is forbidden across all workflows).
2. **Short & Punchy Videos**: Long clips (>20s) kill completion rates. Keep memes <8s and streamer clips <15s.
3. **No External Watermarks**: Client videos must never have TikTok/CapCut/third-party logos.
4. **Desktop Link Logging**: Whenever a Preme clip is posted, append the URL to `preme_clipping_links.txt` for payout tracking on clipping.net.

---

## 🛠️ Local Quick Start

```bash
# Clone
git clone https://github.com/Vivekrawat16/ai-coding-assistant-for-editing.git
cd ai-coding-assistant-for-editing

# Install dependencies
pip install -r requirements.txt

# Run Personal Topic Clustering Loop (generates 3 spin-offs to Drive)
python personal/generator/cluster_pipeline.py 3

# Run Client Preme Pipeline (scrapes Twitch, renders 14s reels, uploads to Drive)
python client/pipeline.py 3
```
