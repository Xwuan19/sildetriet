from PIL import Image

im = Image.open("preview_red/lenin_full_clean_raw.png")
for y in range(160, 245, 10):
    for x in range(400, 650):
        r, g, b = im.getpixel((x, y))[:3]
        if (r > 90) and (g < 25) and (b < 25) and (r - g > 65):
            print(f"y={y}: red flag starts at x={x}, color={(r, g, b)}")
            break
