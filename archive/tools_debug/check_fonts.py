# -*- coding: utf-8 -*-
import hashlib
import os
from pathlib import Path

from fontTools.ttLib import TTFont

local = Path(__file__).resolve().parent.parent / "fonts"
installed = Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts"

for name in ("PlayfairDisplayPoster.ttf", "PlayfairDisplayPoster-Italic.ttf"):
    for label, folder in (("local", local), ("installed", installed)):
        path = folder / name
        if not path.exists():
            print(f"{label:9s} {name}: MISSING")
            continue
        font = TTFont(str(path))
        names = {}
        for rec in font["name"].names:
            if rec.nameID in (1, 2, 4, 16, 17):
                names.setdefault(rec.nameID, set()).add(rec.toUnicode())
        print(f"{label:9s} {name}: weight={font['OS/2'].usWeightClass} "
              f"sha={hashlib.sha1(path.read_bytes()).hexdigest()[:10]}")
        for k in sorted(names):
            print(f"    id{k}: {sorted(names[k])}")
