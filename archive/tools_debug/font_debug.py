# -*- coding: utf-8 -*-
from pathlib import Path

from fontTools.ttLib import TTFont

path = Path(__file__).resolve().parent.parent / "fonts" / "PlayfairDisplayPoster.ttf"
font = TTFont(str(path))
print("tables:", sorted(font.keys()))
print("fvar:", "fvar" in font, "STAT:", "STAT" in font)
for rec in font["name"].names:
    try:
        value = rec.toUnicode()
    except Exception:
        value = "?"
    print(f"id={rec.nameID:3d} plat={rec.platformID} enc={rec.platEncID} lang={rec.langID:04x} {value!r}")
