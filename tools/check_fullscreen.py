from PIL import Image
import glob

# Check corners and borders of f_001 to f_058
# The background around the monitor in f_004 is beige (around 220, 210, 195).
# Let's see if any frame has different border colors (e.g. pure red or full screen slide).

beige_count = 0
for path in sorted(glob.glob("preview_red/video_1080p_frames/f_*.png")):
    im = Image.open(path)
    # Check top-left corner (pixel at 10, 10)
    p = im.getpixel((10, 10))
    # If it's beige:
    if p[0] > 180 and p[1] > 170 and p[2] > 150:
        beige_count += 1
    else:
        print(f"Frame {path} has corner pixel {p}")

print(f"Total frames: {len(glob.glob('preview_red/video_1080p_frames/f_*.png'))}, Beige background frames: {beige_count}")
