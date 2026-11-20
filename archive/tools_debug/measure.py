# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build_deck as b

items = [
    ("TRIẾT HỌC", "display", 96, -1.5),
    ("MÁC – LÊNIN", "display", 96, -1.5),
    ("CHÚNG", "display", 92, -1.2),
    ("TÔI", "display", 112, -1.2),
    ("CẢM", "display", 168, -2.0),
    ("ƠN", "display", 168, -2.0),
    ("Kính chào thầy cô và các bạn", "script", 32, 0.2),
    ("năm người, một cách nhìn", "script", 28, 0),
    ("và hẹn gặp lại ở Chương 1", "script", 30, 0),
]
for text, key, pt, spc in items:
    print(f"{text!r:40s} {pt:>4}pt -> {b.measure(text, key, pt):.2f} in")

print("fit TRIẾT HỌC:", b.fit("TRIẾT HỌC", "display", 6.55, 96, 56, -1.5))
print("fit MÁC – LÊNIN:", b.fit("MÁC – LÊNIN", "display", 7.55, 96, 56, -1.5))
