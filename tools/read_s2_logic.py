# -*- coding: utf-8 -*-
# Let's inspect Slide 2 card generation logic in build_deck.py
with open("build_deck.py", "r", encoding="utf-8") as f:
    code = f.read()

import re
m = re.search(r"def build_slide_2.*?(?=def build_slide_3)", code, re.DOTALL)
if m:
    print(m.group(0)[:1500])
