import os
from pathlib import Path
from PIL import Image

media_dir = Path("preview_red/slideppt_media")
for f in sorted(media_dir.glob("*.png")):
    im = Image.open(f)
    print(f"{f.name}: size={im.size}, mode={im.mode}")
