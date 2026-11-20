from PIL import Image

im = Image.open("preview_red/lenin_full_clean_raw.png")
for y in range(240, 420, 15):
    # Scan from x=450 to 650
    # In red flag: r > 100, g < 25, b < 25
    # Coat/collar/ear: r < 80 or g > 40 or (r - g) < 55
    edge_x = None
    for x in range(450, 680):
        r, g, b = im.getpixel((x, y))[:3]
        if (r > 100) and (g < 30) and (b < 30) and (r - g > 70):
            # This is red flag!
            edge_x = x
            break
    print(f"y={y}: right edge where red flag starts at x={edge_x}")
