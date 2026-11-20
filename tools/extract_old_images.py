# -*- coding: utf-8 -*-
from pptx import Presentation
import os

prs = Presentation("archive/debug/embed_test.pptx")
os.makedirs("tools_out", exist_ok=True)
for i, s in enumerate(prs.slides):
    for shp in s.shapes:
        if shp.shape_type == 13: # Picture
            img = shp.image
            ext = img.ext
            out_name = f"tools_out/slide_{i+1}_{shp.name}.{ext}"
            with open(out_name, "wb") as f:
                f.write(img.blob)
            print(f"Slide {i+1} picture: {shp.name}, size={shp.width.inches:.2f}x{shp.height.inches:.2f}, saved to {out_name}")
