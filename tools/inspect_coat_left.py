from PIL import Image

im = Image.open("preview_red/lenin_full_clean_raw.png")
for y in range(360, 600, 20):
    for x in range(50, 400):
        r, g, b = im.getpixel((x, y))[:3]
        # In red flag: r > 100, g < 25, b < 25, (r - g) > 80
        # In coat lapel: coat is dark grey/brown! r < 80 or g > 40 or (r - g) < 50
        if (r < 80) or (g > 40) or (r - g < 50):
            print(f"y={y}: coat edge at x={x}, color={(r, g, b)}")
            break
