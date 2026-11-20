import os
from pathlib import Path
import datetime

today = datetime.date(2026, 11, 20)
found = []

for root, dirs, files in os.walk(r"C:\Users\ADMIN"):
    if any(k in root for k in ["node_modules", ".git", ".venv", "AppData\\Local\\Microsoft", "AppData\\Local\\Google"]):
        continue
    for f in files:
        if any(f.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp"]):
            p = Path(root) / f
            try:
                mtime = datetime.date.fromtimestamp(p.stat().st_mtime)
                if mtime == today:
                    found.append((p.stat().st_mtime, p))
            except Exception:
                pass

found.sort(key=lambda x: x[0], reverse=True)
print(f"Found {len(found)} image files today:")
for mtime, p in found[:50]:
    print(f"  {p}")
