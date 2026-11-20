from PIL import Image, ImageChops

for i in range(20, 31):
    im = Image.open(f"preview_red/morph_frames/frame_{i:03d}.png")
    # sample pixel at (100, 100) or check change
    print(f"frame_{i:03d}: size={im.size}")
