from PIL import Image

im = Image.open("preview_red/slide1_t6.0.png")
w, h = im.size

# Check the black monitor bezel
# Look at row 60, row 65, row 70, row 75
for y in range(40, 85, 5):
    print(f"y={y}: x=115:{im.getpixel((115, y))[:3]}, x=125:{im.getpixel((125, y))[:3]}, x=960:{im.getpixel((960, y))[:3]}")

# Look at bottom
for y in range(970, 1020, 5):
    print(f"y={y}: x=960:{im.getpixel((960, y))[:3]}")
