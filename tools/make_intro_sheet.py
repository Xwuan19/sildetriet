from pathlib import Path
from PIL import Image

# Let's inspect intro_frames f_001 to f_035
sheet = Image.new("RGB", (5 * 320, 3 * 180))
idx = 0
for f_num in range(1, 31, 2):
    f_path = Path(f"preview_red/intro_frames/f_{f_num:03d}.png")
    if f_path.exists():
        im = Image.open(f_path).resize((320, 180))
        r = idx // 5
        c = idx % 5
        sheet.paste(im, (c * 320, r * 180))
        idx += 1

sheet.save("preview_red/intro_0_3.png")
print("Saved intro_0_3.png")
