import os
from pathlib import Path
import time

now = time.time()
found = []

# Search in C:\Users\ADMIN\.antigravity or AppData or current dir
search_roots = [
    Path(r"C:\Users\ADMIN\.antigravity"),
    Path(r"C:\Users\ADMIN\AppData\Roaming"),
    Path(r"C:\Users\ADMIN\Downloads")
]

for sroot in search_roots:
    if not sroot.exists():
        continue
    for root, dirs, files in os.walk(sroot):
        # skip git and node_modules
        if ".git" in root or "node_modules" in root:
            continue
        for f in files:
            if any(f.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
                p = Path(root) / f
                try:
                    mtime = p.stat().st_mtime
                    if now - mtime < 600: # 10 min
                        found.append((mtime, p))
                except Exception:
                    pass

found.sort(key=lambda x: x[0], reverse=True)
print(f"Found {len(found)} files:")
for mtime, p in found[:30]:
    print(f"  {time.strftime('%H:%M:%S', time.localtime(mtime))} - {p}")
