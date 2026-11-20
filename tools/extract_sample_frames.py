# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ff = r"C:\Program Files (x86)\FreeDownloadManager.ORG\Free Download Manager\ffmpeg.exe"
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
out = Path(r"C:\Users\ADMIN\Downloads\sildetriet\preview_red\sample_frames")
out.mkdir(parents=True, exist_ok=True)
for f in out.glob("*"):
    try:
        f.unlink()
    except Exception:
        pass

# probe
r = subprocess.run([ff, "-i", video], capture_output=True, text=True, encoding="utf-8", errors="replace")
print((r.stderr or "")[:3000])

# extract 1 fps
cmd = [ff, "-y", "-i", video, "-vf", "fps=1,scale=1280:-1", str(out / "frame_%03d.jpg")]
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
print("RETURN", r.returncode)
print((r.stderr or "")[-1500:])

files = sorted(out.glob("*.jpg"))
print("COUNT", len(files))
for f in files[:20]:
    print(f.name, f.stat().st_size)
