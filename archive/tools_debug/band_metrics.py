# -*- coding: utf-8 -*-
"""Đo dải mực chữ (kem/vàng) theo hàng, lọc nhiễu mảnh mảnh."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
PNG = ROOT / "preview_red" / "png"


def analyze(img, x0, x1, y0, y1, label):
    crop = np.array(img.crop((int(x0 * 144), int(y0 * 144), int(x1 * 144), int(y1 * 144))))
    r, g, b = crop[:, :, 0].astype(int), crop[:, :, 1].astype(int), crop[:, :, 2].astype(int)
    gold = (r > 165) & (g > 110) & (b < 160) & (r - b > 50)
    cream = (r > 215) & (g > 200) & (b > 170) & (np.abs(r - g) < 45)
    mask = gold | cream
    rows = mask.sum(axis=1)
    min_px = max(6, int(0.015 * crop.shape[1]))
    active = rows > min_px
    print(f"\n{label}: x {x0}-{x1} in")
    start = None
    for i, on in enumerate(active):
        if on and start is None:
            start = i
        elif not on and start is not None:
            top, bottom = y0 + start / 144, y0 + i / 144
            if bottom - top > 0.025:
                print(f"  {top:5.2f} – {bottom:5.2f} in  (cao {bottom - top:.2f})")
            start = None
    if start is not None:
        print(f"  {y0 + start / 144:5.2f} – {y1:5.2f} in")


for n in (1, 2, 3):
    img = Image.open(PNG / f"Slide {n}.PNG").convert("RGB")
    print(f"\n===== SLIDE {n} =====")
    if n == 1:
        analyze(img, 0.7, 8.0, 1.0, 6.7, "cột trái")
    elif n == 2:
        analyze(img, 0.7, 8.5, 1.2, 6.8, "cột trái")
    else:
        analyze(img, 0.7, 7.5, 1.2, 6.9, "cột trái")
