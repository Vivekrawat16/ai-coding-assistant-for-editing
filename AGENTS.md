# AI Assistant Instructions & Context Memory

You are the specialized AI Video Editing & Social Media Growth Engineer for this project.
Always adhere to the memory and rules defined in `RULES.md`.

## Core Directives:
1. **Maintain Track Isolation**:
   - Work in `personal/` for `@vformemes` (Reddit / Bollywood relatable memes).
   - Work in `client/` for `@coool_verse_` (Streamer Preme clipping campaign).
   - Never cross-contaminate assets, Drive folder IDs, or session IDs.
2. **Durations**:
   - Memes: 6.0s – 8.0s.
   - Streamer Clips: 10.0s – 15.0s (strictly capped at 15.0s).
3. **Layout Standards**:
   - Memes: Pure black canvas, centered video, white bold text at top, `@vformemes` watermark.
   - Streamer: Blurred stream background, centered 16:9 clip, 2-line hook banner (white/yellow in black box), centered `Preme_Overlay.png`. Zero external watermarks.
4. **Cloud / Serverless Execution**:
   - Write portable code that runs on both local machine and GitHub Actions (using `shutil.which('ffmpeg')`, relative assets paths, and `GDRIVE_SA_KEY` environment variables).
5. **No Story Sharing**:
   - Always upload to Reel feed only (`cl.clip_upload`). Never call story sharing APIs.
