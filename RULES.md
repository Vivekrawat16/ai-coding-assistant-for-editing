# AI Video Editing Assistant - Master Rules & Memory

This repository contains the persistent memory, guidelines, layout formulas, and code pipelines for AI coding assistants working on short-form video automations.

---

## 🧭 Core Architectural Guidelines

### 1. Dual Track Isolation (Personal vs Client)
Never mix assets, credentials, Drive folders, or logic between these two tracks:

| Parameter | Track 1: Personal (Reddit Memes) | Track 2: Client Clipping (Streamer Preme) |
| :--- | :--- | :--- |
| **Target Account** | `@vformemes` (PK: `56489482147`) | `@coool_verse_` (PK: `39514790939`) |
| **Content Theme** | Relatable Desi/Indian Pop-culture Memes | Viral Streamer Moments (Twitch / Kick) |
| **Canvas** | 1080x1920 (Pure Black Background) | 1080x1920 (Blurred/Darkened Stream Video) |
| **Video Ratio** | 16:9 (1080x608) or 4:3 (1080x810) Centered | 16:9 (1080x608) Centered at `y=656` |
| **Duration** | **6.0 to 8.0 seconds** (Fast loop) | **10.0 to 15.0 seconds** (Strict 15s max) |
| **Header / Hook** | Clean white text (Montserrat-Bold 42pt) | 2-Line Bold Banner (White + Yellow, Black box) |
| **Branding** | Subtle `@vformemes` watermark at bottom | Official `Preme_Overlay.png` centered below video |
| **Watermark Rule** | `@vformemes` only | **Zero third-party watermarks** (Mandatory) |
| **Google Drive Queue** | `15tEG1buRhHi8g4lkv98KMJC_-LHupuvV` | `1NuU7Jc3zLVnd08UZh6U-2QrlWxOmEWXr` |
| **Google Drive Archive**| `19oTHwlAxucPomUfLXAOanyDyzTMeshya` | `1E3xbmMxuMykWskFagbQ155mn5Dq1QWfG` |
| **Special Mechanism** | 2-Day Topic Clustering Feedback Loop | clipping.net bounty ($50/100K views) |

---

## 🚫 Absolute Hard Constraints

1. **NO STORY SHARING**:
   * All automations must upload directly to the Instagram Reel feed ONLY (`cl.clip_upload`).
   * Never call `cl.media_share_to_story()`.
2. **DURATION CAP**:
   * Long videos (>20s) suffer drop-offs on Instagram Reels. Preme clips must be capped at 15.0 seconds max. Memes capped at 7.5 seconds max.
3. **SAFE ZONE CENTERING**:
   * Video and hook text must stay inside the Instagram UI safe zone (between `y=400` and `y=1500`) so they are never covered by user handles, captions, or right-side engagement buttons.

---

## 🎨 FFmpeg Compositing Recipes

### Layout A: Centered Dark Meme (Personal)
```bash
ffmpeg -y -i raw_character.mp4 -i text_overlay.png -t 7.0 \
  -filter_complex "\
    color=c=black:s=1080x1920:d=7.0[bg]; \
    [0:v]scale=1080:608:force_original_aspect_ratio=increase,crop=1080:608,format=yuv420p[vid]; \
    [bg][vid]overlay=0:680[comp]; \
    [comp][1:v]overlay=0:0[vfinal]; \
    [0:a]atrim=0:7.0,afade=t=out:st=5.8:d=1.2[afinal]" \
  -map "[vfinal]" -map "[afinal]" -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p output.mp4
```

### Layout B: Streamer Clip with Blurred Background & Overlay (Client)
```bash
ffmpeg -y -i raw_stream_clip.mp4 -i Preme_Overlay.png -t 14.0 \
  -filter_complex "\
    [0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=35,colorlevels=rimin=0.2:gimin=0.2:bimin=0.2[bg]; \
    [0:v]scale=1080:608:force_original_aspect_ratio=increase,crop=1080:608,format=yuv420p[center_vid]; \
    [bg][center_vid]overlay=0:656[comp1]; \
    [comp1]drawtext=text='HOOK LINE 1':fontfile='font.ttf':fontsize=44:fontcolor=white:box=1:boxcolor=black@0.75:boxborderw=14:x=(w-text_w)/2:y=420,drawtext=text='HOOK LINE 2':fontfile='font.ttf':fontsize=44:fontcolor=yellow:box=1:boxcolor=black@0.75:boxborderw=14:x=(w-text_w)/2:y=486[comp2]; \
    [1:v]scale=1080:1920[overlay]; \
    [comp2][overlay]overlay=0:0[vfinal]; \
    [0:a]atrim=0:14.0,afade=t=out:st=12.8:d=1.2[afinal]" \
  -map "[vfinal]" -map "[afinal]" -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p output.mp4
```

---

## 📈 Algorithmic Feedback Loop Formula
For `@vformemes`, every 2 days:
1. Audit last 15 reels: `Score = Views + (Likes × 10) + (Comments × 20)`.
2. Categorize topics: `chaar_log_relatives`, `landlord_pg`, `corporate_majdoori`, `startup_hustle`, `general_desi_meme`.
3. Pick winning topic with highest average score.
4. Generate 3 spin-off reels clustered on winning topic.
5. Push to Google Drive Queue for scheduled posting.
