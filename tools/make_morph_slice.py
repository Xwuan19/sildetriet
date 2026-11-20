from PIL import Image
from pathlib import Path

frames_dir = Path("preview_red/ref_frames_hd")
# Let's inspect frames 50 to 90 at intervals of 4
sheet = Image.new("RGB", (5 * 320, 2 * 180))
idx = 0
for f_num in range(55, 95, 4):
    f_path = frames_dir / f"f_{f_num:04d}.png"
    if f_path.exists():
        im = Image.open(f_path).resize((320, 180))
        r = idx // 5
        c = idx % 5
        sheet.paste(im, (c * 320, r * 180))
        idx += 1

sheet.save("preview_red/morph_55_95.png")
print("Saved morph_55_95.png")
