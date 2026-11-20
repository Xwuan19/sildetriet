from pathlib import Path
from PIL import Image, ImageChops

frames = sorted(Path("preview_red/morph_frames").glob("frame_*.png"))
for i in range(len(frames) - 1):
    im1 = Image.open(frames[i])
    im2 = Image.open(frames[i+1])
    diff = ImageChops.difference(im1, im2)
    bbox = diff.getbbox()
    if bbox:
        print(f"Diff between {frames[i].name} and {frames[i+1].name}")
