from PIL import Image

im = Image.open("preview_red/slide1_t6.0.png")
# Look at y from 990 to 1030
for y in range(990, 1040):
    p = im.getpixel((960, y))
    print(f"y={y}: {p[:3]}")
