from pathlib import Path
from PIL import Image

sec_dir = Path("preview_red/all_seconds")
secs = sorted(list(sec_dir.glob("sec_*.png")))

# Let's create a contact sheet of all seconds (e.g. 58 seconds)
cols = 8
rows = (len(secs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 160, rows * 90))

for idx, s in enumerate(secs):
    im = Image.open(s).resize((160, 90))
    r = idx // cols
    c = idx % cols
    sheet.paste(im, (c * 160, r * 90))

sheet.save("preview_red/all_seconds_grid.png")
print("Saved all_seconds_grid.png")
