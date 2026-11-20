from PIL import Image, ImageDraw
from pathlib import Path

media_dir = Path("preview_red/slideppt_media")
sheet = Image.new("RGB", (4 * 320, 4 * 180), (30, 30, 30))
draw = ImageDraw.Draw(sheet)

for idx, p in enumerate(sorted(media_dir.glob("*.png"))):
    im = Image.open(p).resize((320, 180))
    r = idx // 4
    c = idx % 4
    x = c * 320
    y = r * 180
    sheet.paste(im, (x, y))
    draw.rectangle([x+4, y+4, x+120, y+24], fill=(0,0,0,200))
    draw.text((x+8, y+6), p.name, fill=(255,255,0))

sheet.save("preview_red/labeled_media_sheet.png")
print("Saved labeled_media_sheet.png")
