import pptx

p1 = r"C:\Users\ADMIN\Downloads\SlidePPT\Mau_Slide_Triet_Hoc_Mac_Lenin_Morph.pptx"
prs1 = pptx.Presentation(p1)
print(f"File 1: {len(prs1.slides)} slides")
for idx, s in enumerate(prs1.slides):
    print(f"  Slide {idx+1}: {len(s.shapes)} shapes")
    for sh in s.shapes[:10]:
        print(f"    - name='{sh.name}', type={sh.shape_type}")

p2 = r"C:\Users\ADMIN\Downloads\SlidePPT\Mau_Slide_Triet_Hoc_Mac_Lenin_Chuan_Morph.pptx"
prs2 = pptx.Presentation(p2)
print(f"\nFile 2: {len(prs2.slides)} slides")
for idx, s in enumerate(prs2.slides):
    print(f"  Slide {idx+1}: {len(s.shapes)} shapes")
