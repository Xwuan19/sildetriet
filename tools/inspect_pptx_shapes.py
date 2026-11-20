from pptx import Presentation

prs = Presentation(r"C:\Users\ADMIN\Downloads\SlidePPT\Mau_Slide_Triet_Hoc_Mac_Lenin_Morph.pptx")
print(f"Total slides: {len(prs.slides)}")
for i, slide in enumerate(prs.slides):
    print(f"\n--- Slide {i+1} ---")
    print(f"Shape count: {len(slide.shapes)}")
    for j, shape in enumerate(slide.shapes):
        text = shape.text.strip().replace('\n', ' ') if shape.has_text_frame else ""
        text_preview = f' text="{text[:40]}"' if text else ""
        print(f"  [{j}] name='{shape.name}', type={shape.shape_type}{text_preview}")
