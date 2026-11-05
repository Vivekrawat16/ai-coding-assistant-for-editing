#!/usr/bin/env python3
"""
Google Drive Uploader for Podcast Clipping
Supports both Google Drive Service Account API and gdrive CLI.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import config

def upload_via_service_account(file_path: str, parent_folder_id: str) -> Optional[str]:
    """Uploads file using Google Drive API and Service Account JSON key."""
    if not config.GDRIVE_SA_KEY:
        return None

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        sa_info = json.loads(config.GDRIVE_SA_KEY)
        creds = service_account.Credentials.from_service_account_info(
            sa_info,
            scopes=["https://www.googleapis.com/auth/drive"]
        )
        service = build("drive", "v3", credentials=creds)

        file_metadata = {
            "name": os.path.basename(file_path),
            "parents": [parent_folder_id]
        }
        media = MediaFileUpload(file_path, mimetype="video/mp4", resumable=True)
        file_obj = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, name"
        ).execute()

        drive_id = file_obj.get("id", "")
        print(f"  ☁️ [Drive API] Uploaded {os.path.basename(file_path)} (ID: {drive_id})")
        return drive_id
    except Exception as e:
        print(f"  ⚠️ Service account upload error: {e}")
        return None

def upload_via_gdrive_cli(file_path: str, parent_folder_id: str) -> Optional[str]:
    """Uploads file using gdrive CLI if installed and authenticated."""
    cmd = ["gdrive", "mutate", "upload", file_path, "--parent", parent_folder_id, "--json"]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            out = res.stdout.strip()
            print(f"  ☁️ [gdrive CLI] Uploaded: {out}")
            if "ID: " in out:
                return out.split("ID: ")[-1].replace(")", "").strip()
            return "SUCCESS"
    except Exception:
        pass
    return None

def upload_to_drive_queue(file_path: str, folder_id: Optional[str] = None) -> Optional[str]:
    target_folder = folder_id or config.GDRIVE_QUEUE_FOLDER_ID
    if not target_folder:
        print("  ℹ️ No Google Drive folder configured. Kept in local output directory.")
        return None

    # Try Service Account first, then gdrive CLI
    res = upload_via_service_account(file_path, target_folder)
    if not res:
        res = upload_via_gdrive_cli(file_path, target_folder)
    return res

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        upload_to_drive_queue(test_file)
