# -*- coding: utf-8 -*-
from pptx import Presentation

prs = Presentation("archive/debug/embed_test.pptx")
print("Slide count:", len(prs.slides))
for i, s in enumerate(prs.slides):
    print(f"\n--- Slide {i+1} Shapes ---")
    for shp in s.shapes:
        x = round(shp.left.inches, 2)
        y = round(shp.top.inches, 2)
        w = round(shp.width.inches, 2)
        h = round(shp.height.inches, 2)
        print(f"  {shp.name:25s} pos=({x:5.2f}, {y:5.2f}) size=({w:4.2f}, {h:4.2f})")
