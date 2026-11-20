import os
from pathlib import Path
import time

now = time.time()
found = []

# Check user profile directory for any image modified in the last 10 minutes
profile = Path(r"C:\Users\ADMIN")
for root, dirs, files in os.walk(profile):
    # skip heavy folders
    if any(skip in root for skip in ["node_modules", ".git", "AppData\\Local\\Microsoft", "AppData\\Local\\Google", "AppData\\Local\\Package"]):
        continue
    for f in files:
        if any(f.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp"]):
            p = Path(root) / f
            try:
                mtime = p.stat().st_mtime
                if now - mtime < 400: # last ~6 mins
                    found.append((mtime, p))
            except Exception:
                pass

found.sort(key=lambda x: x[0], reverse=True)
print(f"Found {len(found)} image files created in last 6 minutes:")
for mtime, p in found[:30]:
    print(f"  {time.strftime('%H:%M:%S', time.localtime(mtime))} - {p}")
