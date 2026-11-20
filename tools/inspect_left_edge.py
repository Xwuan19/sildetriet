from PIL import Image

im = Image.open("preview_red/lenin_full_clean_raw.png")
# Scan left boundary: for each row y, find first pixel belonging to Lenin
for y in range(40, 750, 40):
    for x in range(0, 400, 5):
        r, g, b = im.getpixel((x, y))[:3]
        # In red flag background:
        # r > 80, g < 25, b < 25 (very red!)
        # Lenin's hat/face/coat has higher g or b or darker r
        if (g > 30) or (b > 30) or (r < 70) or (r - g < 50):
            print(f"y={y}: left edge at x={x}, color={r, g, b}")
            break
