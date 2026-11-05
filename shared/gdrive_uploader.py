#!/usr/bin/env python3
"""
Universal Google Drive Uploader
Supports:
1. Google Drive API via Service Account (GDRIVE_SA_KEY env) for Serverless Cloud / GitHub Actions
2. Local gdrive CLI (gdrive mutate upload)
"""

import os
import json
import shutil
import subprocess
from typing import Optional

GDRIVE_SA_KEY = os.getenv("GDRIVE_SA_KEY", "")

def upload_via_service_account(file_path: str, parent_folder_id: str) -> Optional[str]:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    try:
        sa_info = json.loads(GDRIVE_SA_KEY)
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
        file_obj = service.files().create(body=file_metadata, media_body=media, fields="id, name").execute()
        drive_id = file_obj.get("id", "")
        print(f"  ☁️ [Drive API] Uploaded {os.path.basename(file_path)} (ID: {drive_id})")
        return drive_id
    except Exception as e:
        print(f"  ❌ Drive API upload failed: {e}")
        return None

def upload_via_gdrive_cli(file_path: str, parent_folder_id: str) -> Optional[str]:
    cmd = ["gdrive", "mutate", "upload", file_path, "--parent", parent_folder_id, "--json"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        out = res.stdout.strip()
        print(f"  ☁️ [gdrive CLI] {out}")
        if "ID: " in out:
            return out.split("ID: ")[-1].replace(")", "").strip()
    else:
        print(f"  ❌ gdrive CLI error: {res.stderr}")
    return None

def upload_to_drive(file_path: str, parent_folder_id: str) -> Optional[str]:
    """Uploads file to Google Drive using available credentials."""
    if GDRIVE_SA_KEY:
        return upload_via_service_account(file_path, parent_folder_id)
    if shutil.which("gdrive"):
        return upload_via_gdrive_cli(file_path, parent_folder_id)
    print("  ⚠️ No Google Drive upload method available (neither GDRIVE_SA_KEY nor gdrive CLI).")
    return None
