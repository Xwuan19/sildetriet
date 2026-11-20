from pathlib import Path
from PIL import Image

media_dir = Path("preview_red/slideppt_media")
for img_path in sorted(media_dir.glob("*.png")):
    im = Image.open(img_path)
    print(f"{img_path.name}: size = {im.size}, mode = {im.mode}")
