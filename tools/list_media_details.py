import os
from pathlib import Path
from PIL import Image

media_dir = Path("preview_red/slideppt_media")
for p in sorted(media_dir.glob("*")):
    if p.is_file():
        im = Image.open(p)
        print(f"{p.name}: size={im.size}, mode={im.mode}")
