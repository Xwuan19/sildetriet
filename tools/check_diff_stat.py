from PIL import Image, ImageStat, ImageChops

im1 = Image.open("preview_red/morph_frames/frame_001.png")
for i in range(1, 77):
    imi = Image.open(f"preview_red/morph_frames/frame_{i:03d}.png")
    diff = ImageChops.difference(im1, imi)
    stat = ImageStat.Stat(diff)
    print(f"frame_{i:03d}: mean diff = {sum(stat.mean)/3:.2f}")
