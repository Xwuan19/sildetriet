from PIL import Image, ImageChops

im1 = Image.open("preview_red/morph_frames/frame_001.png")
for i in range(1, 77):
    imi = Image.open(f"preview_red/morph_frames/frame_{i:03d}.png")
    diff = ImageChops.difference(im1, imi)
    bbox = diff.getbbox()
    if bbox:
        print(f"First diff from frame 1 at: frame_{i:03d}.png")
        break
