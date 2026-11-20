# -*- coding: utf-8 -*-
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

for name in ("PlayfairDisplay-Black.ttf", "PlayfairDisplay-BlackItalic.ttf",
             "DancingScript-Bold.ttf", "BeVietnamPro-SemiBold.ttf"):
    path = Path(__file__).resolve().parent.parent / "fonts" / name
    font = TTFont(str(path))
    print("==", name, "weight", font["OS/2"].usWeightClass, "fsSelection",
          bin(font["OS/2"].fsSelection))
    for rec in font["name"].names:
        if rec.nameID in (1, 2, 4, 6, 16, 17):
            try:
                value = rec.toUnicode()
            except Exception:
                value = "?"
            print(f"  id={rec.nameID:2d} plat={rec.platformID} enc={rec.platEncID} lang={rec.langID:04x} {value!r}")
