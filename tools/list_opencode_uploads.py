import os
from pathlib import Path

uploads_dir = Path(r"C:\Users\ADMIN\AppData\Local\Temp\opencode\uploads")
if uploads_dir.exists():
    for root, dirs, files in os.walk(uploads_dir):
        for f in files:
            p = Path(root) / f
            print(f"{p.stat().st_mtime} - {p} ({p.stat().st_size} bytes)")
