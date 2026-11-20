from pptx import Presentation
from pathlib import Path

pptx_path = Path(r"C:\Users\ADMIN\Downloads\SlidePPT\Mau_Slide_Triet_Hoc_Mac_Lenin_Chuan_Morph.pptx")
prs = Presentation(pptx_path)

print(f"Total slides: {len(prs.slides)}")
for idx, slide in enumerate(prs.slides):
    if idx >= 4:
        break
    print(f"\n--- Slide {idx+1} --- (shapes: {len(slide.shapes)})")
    for s_idx, shape in enumerate(slide.shapes):
        print(f"  [{s_idx}] Name: '{shape.name}' pos: ({shape.left.inches:.2f}, {shape.top.inches:.2f}, {shape.width.inches:.2f}, {shape.height.inches:.2f})")
