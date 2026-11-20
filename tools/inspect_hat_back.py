from PIL import Image

im = Image.open("preview_red/lenin_full_clean_raw.png")
for y in range(120, 180, 10):
    row = [im.getpixel((x, y))[:3] for x in range(480, 620, 10)]
    print(f"y={y}:")
    for i, p in enumerate(row):
        x = 480 + i * 10
        # If dark hat: sum < 150
        print(f"  x={x}: {p}")
