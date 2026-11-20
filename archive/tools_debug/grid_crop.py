# -*- coding: utf-8 -*-
"""Cắt vùng slide và chồng lưới 0,25 inch có nhãn để đo bằng mắt."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
PNG = ROOT / "preview_red" / "png"
DPI = 144

font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 18)


def grid(n, x0, x1, y0, y1, out):
    im = Image.open(PNG / f"Slide {n}.PNG").convert("RGB")
    crop = im.crop((int(x0 * DPI), int(y0 * DPI), int(x1 * DPI), int(y1 * DPI)))
    draw = ImageDraw.Draw(crop)
    y = y0
    while y <= y1 + 0.001:
        py = int((y - y0) * DPI)
        draw.line([(0, py), (crop.width, py)], fill=(0, 255, 255), width=1)
        draw.text((4, py + 1), f"{y:.2f}", fill=(0, 255, 255), font=font)
        y = round(y + 0.25, 3)
    x = x0
    while x <= x1 + 0.001:
        px = int((x - x0) * DPI)
        draw.line([(px, 0), (px, crop.height)], fill=(0, 255, 255), width=1)
        draw.text((px + 2, 2), f"{x:.2f}", fill=(0, 255, 255), font=font)
        x = round(x + 0.5, 3)
    crop.save(ROOT / "preview_red" / out)
    print(out, crop.size)


grid(3, 0.6, 7.4, 1.2, 5.8, "grid_slide3.png")
grid(2, 0.6, 8.4, 1.2, 6.8, "grid_slide2.png")
grid(1, 0.6, 8.4, 1.1, 5.6, "grid_slide1.png")
