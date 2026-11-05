#!/usr/bin/env python3
"""
Official YouTube Shorts Uploader
Uses Google YouTube Data API v3 with OAuth 2.0.
Supports one-time local authentication, automatic token refresh,
and autonomous cloud uploads (GitHub Actions).
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import config

CLIENT_SECRETS_FILE = BASE_DIR / "client_secret.json"
TOKEN_FILE = BASE_DIR / "yt_token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]

def get_authenticated_service():
    """Authenticates with YouTube API using OAuth 2.0."""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None

    # Check if cloud secret is in environment variable
    env_token = os.getenv("YOUTUBE_TOKEN_JSON")
    if env_token:
        try:
            token_data = json.loads(env_token)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except Exception as e:
            print(f"⚠️ Error parsing YOUTUBE_TOKEN_JSON from env: {e}")

    # Check local token file
    if not creds and TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception as e:
            print(f"⚠️ Error reading {TOKEN_FILE}: {e}")

    # Refresh or run auth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired YouTube access token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"❌ Token refresh failed: {e}")
                creds = None

        if not creds:
            if not CLIENT_SECRETS_FILE.exists():
                print("=" * 65)
                print("❌ MISSING 'client_secret.json'!")
                print("To upload to YouTube automatically, you need Google OAuth credentials:")
                print("1. Go to https://console.cloud.google.com/apis/credentials")
                print("2. Create OAuth Client ID -> Application Type: 'Desktop app'")
                print("3. Download JSON and save as:")
                print(f"   {CLIENT_SECRETS_FILE}")
                print("=" * 65)
                return None

            print("🔑 Starting one-time YouTube OAuth authentication in browser...")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
            creds = flow.run_local_server(port=8088, prompt="consent", access_type="offline")

        # Save tokens
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print(f"✅ Saved authentication token to {TOKEN_FILE}")

    return build("youtube", "v3", credentials=creds)

def upload_short(
    video_path: str,
    title: str,
    description: str = "",
    tags: Optional[List[str]] = None,
    privacy_status: str = "public",
    category_id: str = "24"
) -> Optional[Dict]:
    """
    Uploads a video to YouTube with #Shorts optimization.
    """
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError

    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return None

    youtube = get_authenticated_service()
    if not youtube:
        return None

    # Guarantee #Shorts in title and description
    clean_title = title.strip()
    if "#Shorts" not in clean_title and "#shorts" not in clean_title:
        clean_title = f"{clean_title[:80]} #Shorts"

    final_tags = tags or ["shorts", "podcast", "interview", "motivation", "clips"]
    if "shorts" not in [t.lower() for t in final_tags]:
        final_tags.append("shorts")

    body = {
        "snippet": {
            "title": clean_title[:100],
            "description": f"{description}\n\n#Shorts #Podcast #Clips",
            "tags": final_tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(
        video_path,
        mimetype="video/mp4",
        chunksize=1024 * 1024 * 2,  # 2MB chunks
        resumable=True
    )

    print(f"🚀 Uploading Short to YouTube: '{clean_title}' ({privacy_status})...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    retry_count = 0
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"  Uploading: {int(status.progress() * 100)}%")
        except HttpError as e:
            if e.resp.status in [500, 502, 503, 504]:
                retry_count += 1
                if retry_count > 5:
                    raise e
                time.sleep(retry_count * 2)
            else:
                raise e

    video_id = response.get("id")
    short_url = f"https://www.youtube.com/shorts/{video_id}"
    print(f"🎉 UPLOAD SUCCESSFUL!")
    print(f"🔗 Live YouTube Short: {short_url}")
    return response

if __name__ == "__main__":
    if len(sys.argv) > 1:
        vid_file = sys.argv[1]
        upload_short(
            video_path=vid_file,
            title="ANDREW TATE ON SUCCESS 💀 #Shorts",
            description="Listen to this very carefully. #Motivation #RawTalk #Podcast",
            privacy_status="public"
        )
    else:
        print("Testing YouTube authentication...")
        srv = get_authenticated_service()
        if srv:
            print("✅ YouTube API is authenticated and ready!")
