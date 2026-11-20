from PIL import Image

im = Image.open("preview_red/lenin_full_clean_raw.png")
for y in range(180, 280, 15):
    print(f"y={y}:")
    for x in range(480, 620, 15):
        p = im.getpixel((x, y))[:3]
        print(f"  x={x}: {p}")
