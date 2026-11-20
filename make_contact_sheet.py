# -*- coding: utf-8 -*-
"""Contact sheet cho bộ 3 slide đỏ – vàng."""
import sys
import unicodedata
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "preview_red" / "final_png"
OUT = ROOT / "preview_red" / "contact_sheet.png"

BG = (34, 4, 8)
GOLD = (244, 223, 163)
GOLD_DIM = (201, 173, 124)
LINE = (120, 82, 38)

thumbs = [Image.open(SRC / f"Slide{i}.PNG").convert("RGB") for i in (1, 2, 3)]
TW = 700
TH = round(TW * 9 / 16)
MARGIN = 30
GAP = 24
HEADER = 112
W = MARGIN * 2 + TW * 3 + GAP * 2
H = HEADER + TH + 64

canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)
title_font = ImageFont.truetype(str(ROOT / "fonts" / "PlayfairEditorial.ttf"), 44)
sub_font = ImageFont.truetype(str(ROOT / "fonts" / "BeVietnamPro-Regular.ttf"), 17)
label_font = ImageFont.truetype(str(ROOT / "fonts" / "BeVietnamPro-SemiBold.ttf"), 16)

draw.text((MARGIN, 22), unicodedata.normalize("NFC", "TRIẾT HỌC MÁC – LÊNIN"),
          font=title_font, fill=GOLD)
draw.text((MARGIN + 2, 78), "Ba slide mở đầu  ·  16:9  ·  Morph 2,2 giây  ·  Đỏ – vàng",
          font=sub_font, fill=GOLD_DIM)
draw.line([(MARGIN, 100), (W - MARGIN, 100)], fill=LINE, width=1)

labels = ["01 · LỜI CHÀO", "02 · ĐỘI NGŨ", "03 · CẢM ƠN"]
for i, (img, label) in enumerate(zip(thumbs, labels)):
    x = MARGIN + i * (TW + GAP)
    y = HEADER
    canvas.paste(img.resize((TW, TH), Image.LANCZOS), (x, y))
    draw.rectangle([x, y, x + TW - 1, y + TH - 1], outline=LINE, width=1)
    draw.text((x + 1, y + TH + 16), label, font=label_font, fill=GOLD)

canvas.save(OUT)
print(f"Đã tạo {OUT.name}: {canvas.size[0]}x{canvas.size[1]}")
