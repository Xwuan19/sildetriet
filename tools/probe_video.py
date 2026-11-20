# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = Path(r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4")
print("exists", p.exists())
if p.exists():
    print("size", p.stat().st_size)
else:
    for c in Path(r"C:\Users\ADMIN\Downloads").iterdir():
        if "Mẫu" in c.name or "Slide" in c.name or "Triết" in c.name:
            print("CANDIDATE", c.name, c.stat().st_size)
