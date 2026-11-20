# -*- coding: utf-8 -*-
from pptx import Presentation

prs = Presentation("archive/debug/embed_test.pptx")
fonts = set()
for s in prs.slides:
    for shp in s.shapes:
        if shp.has_text_frame:
            for p in shp.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.name:
                        fonts.add(r.font.name)
print("Fonts used in embed_test.pptx:")
for f in sorted(fonts):
    print(" -", f)
