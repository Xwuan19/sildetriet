from PIL import Image
from pathlib import Path

media_dir = Path("preview_red/slideppt_media")
for p in sorted(media_dir.glob("*.png")):
    im = Image.open(p)
    print(f"{p.name}: size={im.size}")
