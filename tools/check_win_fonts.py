import os
from pathlib import Path

win_fonts = Path(r"C:\Windows\Fonts")
found = []
for f in win_fonts.glob("*"):
    fn = f.name.lower()
    if any(k in fn for k in ["goth", "fraktur", "old", "cloister", "blackletter", "chancery", "uncial"]):
        found.append(f.name)
print("Found Windows fonts:", found)
