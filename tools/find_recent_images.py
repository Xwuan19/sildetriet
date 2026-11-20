import os
from pathlib import Path
import time

now = time.time()
found = []

# Check temp directories
dirs_to_check = [
    Path(os.environ.get("TEMP", r"C:\Users\ADMIN\AppData\Local\Temp")),
    Path(r"C:\Users\ADMIN\AppData\Local\Temp\antigravity"),
    Path(".")
]

for d in dirs_to_check:
    if d.exists():
        for p in d.rglob("*"):
            if p.is_file() and p.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                try:
                    mtime = p.stat().st_mtime
                    if now - mtime < 600: # last 10 minutes
                        found.append((mtime, p))
                except Exception:
                    pass

found.sort(key=lambda x: x[0], reverse=True)
print(f"Found {len(found)} recent image files:")
for mtime, p in found[:25]:
    print(f"  {time.strftime('%H:%M:%S', time.localtime(mtime))} - {p}")
