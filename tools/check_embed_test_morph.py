# -*- coding: utf-8 -*-
from pptx import Presentation

prs = Presentation("archive/debug/embed_test.pptx")
names_by_slide = []
for i, s in enumerate(prs.slides):
    names = [shp.name for shp in s.shapes]
    names_by_slide.append(set(names))
    print(f"Slide {i+1} shape names count: {len(names)}")

print("\nCommon to all 3 slides:", names_by_slide[0] & names_by_slide[1] & names_by_slide[2])
print("\nSlide 1 only:", names_by_slide[0] - names_by_slide[1] - names_by_slide[2])
print("\nSlide 2 only:", names_by_slide[1] - names_by_slide[0] - names_by_slide[2])
print("\nSlide 3 only:", names_by_slide[2] - names_by_slide[0] - names_by_slide[1])
