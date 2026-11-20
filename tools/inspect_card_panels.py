# -*- coding: utf-8 -*-
with open("build_deck.py", "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect where cards are added in Slide 1, 2, 3
import re
print("Occurrences of CARD_PANEL in build_deck.py:")
for m in re.finditer(r".*CARD_PANEL.*", text):
    print(m.group(0))
