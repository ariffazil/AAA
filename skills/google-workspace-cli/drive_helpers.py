#!/usr/bin/env python3
"""
Google Drive CLI helper — uses Arif's existing OAuth refresh token.
Token auto-refreshes. No browser needed.

Usage:
  python3 drive_helpers.py list "query"
  python3 drive_helpers.py get <file_id>
  python3 drive_helpers.py download <file_id> [local_path]
  python3 drive_helpers.py search "filename"
"""
import sys
import os
import json
import urllib.request
import urllib.parse

TOKEN_FILE = "/root/HERMES/google_token.json"
CLIENT_FILE = "/root/HERMES/google_client_secret.json"

def get_access_token():
    with open(TOKEN_FILE) as f:
        token_data = json.load(f)
    with open(CLIENT_FILE) as f:
        client = json.load(f)["installed"]
    
    # Check if token needs refresh (simple: just refresh always for now)
    import time
    expiry_str = token_data.get("expiry", "")
    if expiry_str:
        try:
            from datetime import datetime, timezone
            expiry = datetime.fromisoformat(expiry_str.replace("Z", "+00:00"))
            if datetime.now(timezone.utc) < expiry:
                return token_data["token"]
        except:
            pass
    
    # Refresh
    data = urllib.parse.urlencode({
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "refresh_token": token_data["refresh_token"],
        "grant_type": "refresh_token"
    }).encode()
    
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    with urllib.request.urlopen(req) as resp:
        new_token = json.loads(resp.read())
    
    # Save new token
    token_data["token"] = new_token["access_token"]
    token_data["expiry"] = new_token.get("expiry", "")
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)
    
    return new_token["access_token"]

def api(method, path, data=None, token=None):
    if token is None:
        token = get_access_token()
    url = f"https://www.googleapis.com/{path}"
    headers = {"Authorization": f"Bearer {token}"}
    if data:
        data = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    token = get_access_token()
    
    if cmd == "list":
        results = api("GET", "drive/v3/files?pageSize=50&fields=files(id,name,mimeType,parents)&q=trashed=false", token=token)
        for f in results.get("files", []):
            print(f"{f['name']} | {f.get('mimeType','?').split('.')[-1]} | {f['id']}")
    
    elif cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        encoded_q = urllib.parse.quote(f"name contains '{query}' and trashed=false")
        results = api("GET", f"drive/v3/files?pageSize=20&fields=files(id,name,mimeType)&q={encoded_q}", token=token)
        for f in results.get("files", []):
            print(f"{f['name']} | {f.get('mimeType','?').split('.')[-1]} | {f['id']}")
    
    elif cmd == "get":
        file_id = sys.argv[2]
        results = api("GET", f"drive/v3/files/{file_id}?fields=id,name,mimeType,parents,createdTime,modifiedTime", token=token)
        print(json.dumps(results, indent=2))
    
    elif cmd == "download":
        file_id = sys.argv[2]
        local_path = sys.argv[3] if len(sys.argv) > 3 else "/tmp/downloaded_file"
        
        # Get file metadata first
        meta = api("GET", f"drive/v3/files/{file_id}?fields=id,name,mimeType", token=token)
        
        if "google-apps" in meta.get("mimeType", ""):
            # Export Google Doc as plain text
            export_mime = "text/plain"
            url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType={export_mime}"
        else:
            url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
        
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
        
        with open(local_path, "wb") as f:
            f.write(content)
        print(f"Downloaded: {meta['name']} -> {local_path} ({len(content)} bytes)")
    
    elif cmd == "read":
        file_id = sys.argv[2]
        meta = api("GET", f"drive/v3/files/{file_id}?fields=id,name,mimeType", token=token)
        
        if "google-apps.document" in meta.get("mimeType", ""):
            url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=text/plain"
        else:
            url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
        
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8", errors="replace")
        print(content[:5000])
    
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: list | search <query> | get <file_id> | download <file_id> [path] | read <file_id>")
