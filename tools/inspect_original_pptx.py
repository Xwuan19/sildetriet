from pptx import Presentation
from pathlib import Path

pptx_path = Path(r"C:\Users\ADMIN\Downloads\SlidePPT\Mau_Slide_Triet_Hoc_Mac_Lenin_Morph.pptx")
prs = Presentation(pptx_path)

print(f"Total slides in original template: {len(prs.slides)}")

for idx, slide in enumerate(prs.slides):
    if idx >= 4:
        break
    print(f"\n--- Slide {idx+1} ---")
    print(f"Shapes count: {len(slide.shapes)}")
    for s_idx, shape in enumerate(slide.shapes):
        text_preview = ""
        try:
            if shape.has_text_frame and shape.text_frame.text:
                text_preview = shape.text_frame.text.replace('\n', ' ')[:40]
        except Exception:
            pass
        name = shape.name
        left = shape.left.inches if shape.left else 0
        top = shape.top.inches if shape.top else 0
        w = shape.width.inches if shape.width else 0
        h = shape.height.inches if shape.height else 0
        shape_type = str(shape.shape_type)
        print(f"  [{s_idx}] Name: '{name}' | Type: {shape_type} | pos: ({left:.2f}, {top:.2f}, {w:.2f}, {h:.2f}) | text: '{text_preview}'")
