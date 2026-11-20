from PIL import Image

im = Image.open("preview_red/slide1_t6.0.png")
# Check row 540 across x:
print("Left side x around 120:")
for x in range(110, 130):
    print(f"x={x}: {im.getpixel((x, 540))[:3]}")

print("Right side x around 1800:")
for x in range(1790, 1810):
    print(f"x={x}: {im.getpixel((x, 540))[:3]}")
