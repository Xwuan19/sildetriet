from PIL import Image

im = Image.open("preview_red/lenin_full_clean_raw.png")
# Let's inspect rows from y=160 to y=350, searching for the edge of the skin/beard
# Print where the skin tone starts (R > 140, G > 60, B > 30)
for y in range(160, 360, 15):
    for x in range(150, 400):
        r, g, b = im.getpixel((x, y))[:3]
        # Skin tone has high green compared to red flag
        # In red flag: g < 20
        # In skin / beard: g > 50 or b > 40
        if g > 50 or (r < 100 and g > 25):
            print(f"y={y}: profile edge at x={x}, color={(r, g, b)}")
            break
