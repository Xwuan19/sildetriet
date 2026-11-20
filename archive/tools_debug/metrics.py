# -*- coding: utf-8 -*-
import sys
from pathlib import Path

from PIL import ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

path = Path(__file__).resolve().parent.parent / "fonts" / "PlayfairEditorial.ttf"
for pt in (156, 168):
    px = int(round(pt * 96 / 72))
    font = ImageFont.truetype(str(path), px)
    print(f"--- {pt}pt ({px}px) ascent/descent={font.getmetrics()}")
    for text in ("CẢM", "ƠN", "TRIẾT HỌC", "MÁC – LÊNIN"):
        print(f"  {text!r:14s} bbox={font.getbbox(text)}")
