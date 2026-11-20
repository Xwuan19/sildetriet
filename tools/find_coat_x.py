from PIL import Image

im = Image.open("preview_red/ref_slide1_clean.png")
# Find where the coat starts at y=800
for x in range(1000, 1300, 10):
    p = im.getpixel((x, 800))
    print(f"x={x}: {p[:3]}")
