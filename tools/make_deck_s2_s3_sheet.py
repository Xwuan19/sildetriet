from PIL import Image
from pathlib import Path

frames_dir = Path("preview_red/deck_morph_s2_s3")
sheet = Image.new("RGB", (5 * 256, 5 * 144))
for i in range(1, 26):
    f_path = frames_dir / f"s3_{i:03d}.png"
    if f_path.exists():
        im = Image.open(f_path).resize((256, 144))
        r = (i - 1) // 5
        c = (i - 1) % 5
        sheet.paste(im, (c * 256, r * 144))

sheet.save("preview_red/deck_s2_s3_sheet.png")
print("Saved deck_s2_s3_sheet.png")
