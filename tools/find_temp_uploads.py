import os
from pathlib import Path
import time

now = time.time()
found = []

# Search everywhere in AppData\Local\Temp
temp_dir = Path(r"C:\Users\ADMIN\AppData\Local\Temp")
for root, dirs, files in os.walk(temp_dir):
    for f in files:
        if any(f.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
            p = Path(root) / f
            try:
                mtime = p.stat().st_mtime
                if now - mtime < 1800: # 30 min
                    found.append((mtime, p))
            except Exception:
                pass

found.sort(key=lambda x: x[0], reverse=True)
print(f"Found {len(found)} in temp:")
for mtime, p in found[:30]:
    print(f"  {time.strftime('%H:%M:%S', time.localtime(mtime))} - {p}")
