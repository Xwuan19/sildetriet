from PIL import Image
from pathlib import Path

media_dir = Path("preview_red/slideppt_media")
sheet = Image.new("RGB", (4 * 320, 4 * 180))
for idx, p in enumerate(sorted(media_dir.glob("*.png"))):
    im = Image.open(p).resize((320, 180))
    r = idx // 4
    c = idx % 4
    sheet.paste(im, (c * 320, r * 180))

sheet.save("preview_red/all_media_sheet.png")
print("Saved all_media_sheet.png")
