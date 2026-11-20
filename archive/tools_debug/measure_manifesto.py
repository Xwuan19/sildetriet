# -*- coding: utf-8 -*-
import sys
from pathlib import Path

from PIL import ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

root = Path(__file__).resolve().parent.parent
font = ImageFont.truetype(str(root / "fonts" / "PlayfairEditorial-Italic.ttf"), int(round(18.5 * 96 / 72)))
for text in (
    "Tư duy phê phán bắt đầu từ việc dám đặt lại câu hỏi.",
    "Mời thầy cô và các bạn bước vào hành trình tư duy phê phán.",
):
    bbox = font.getbbox(text)
    print(f"{text!r} -> {(bbox[2]-bbox[0])/96:.2f} in")
