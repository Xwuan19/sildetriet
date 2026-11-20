# -*- coding: utf-8 -*-
import re
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pptx = Path(__file__).resolve().parent.parent / "Triet_hoc_Mac_Lenin_Loi_chao.pptx"
z = zipfile.ZipFile(pptx)
for i in (1, 2, 3):
    x = z.read(f"ppt/slides/slide{i}.xml").decode("utf-8")
    print(f"slide {i}: morph={'p159:morph' in x} dur={'p14:dur=\"2200\"' in x} "
          f"alt={'AlternateContent' in x}")
    m = re.search(r"<mc:AlternateContent.*?</mc:AlternateContent>", x, re.S)
    print((m.group(0)[:420] if m else "NO ALT"))
