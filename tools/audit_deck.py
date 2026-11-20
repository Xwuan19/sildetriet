# -*- coding: utf-8 -*-
"""Kiểm tra cấu trúc PPTX: layer, font, morph, tràn khung."""
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu
from lxml import etree

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
PPTX = ROOT / "Triet_hoc_Mac_Lenin_Loi_chao.pptx"

# Các layer được thiết kế tràn mép (bleed) — không tính là lỗi.
BLEED = {"GLOW_PORTRAIT", "STAR_BACK", "LENIN_HERO"}

prs = Presentation(str(PPTX))
print(f"slide size: {prs.slide_width / 914400:.3f} x {prs.slide_height / 914400:.3f} in")
print(f"slides: {len(prs.slides)}")

fonts = set()
for idx, slide in enumerate(prs.slides, 1):
    print(f"\n=== Slide {idx}: {len(slide.shapes)} shapes")
    names = set()
    for shp in slide.shapes:
        if shp.name in names:
            print(f"  TRÙNG TÊN: {shp.name}")
        names.add(shp.name)
        if shp.has_text_frame:
            for p in shp.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.name:
                        fonts.add(r.font.name)
        if shp.name in BLEED:
            continue
        right = (shp.left + shp.width) / 914400
        bottom = (shp.top + shp.height) / 914400
        if shp.left < 0 or shp.top < 0 or right > 13.34 or bottom > 7.51:
            print(f"  NGOÀI KHUNG: {shp.name} L={shp.left/914400:.2f} T={shp.top/914400:.2f} "
                  f"R={right:.2f} B={bottom:.2f}")
    print("  layers: " + ", ".join(sorted(names)))

print("\nFonts used:", sorted(fonts))

# morph XML
ns = "{http://schemas.openxmlformats.org/markup-compatibility/2006}"
for idx, slide in enumerate(prs.slides, 1):
    alt = slide._element.findall(ns + "AlternateContent")
    print(f"slide {idx}: AlternateContent={len(alt)}", end="")
    if alt:
        xml = etree.tostring(alt[0], encoding="unicode")
        print(f" morph={'p159:morph' in xml} dur={'2200' in xml}")
    else:
        print()
