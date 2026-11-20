import os
from pathlib import Path
from PIL import Image

for f in sorted(Path("preview_red/slideppt_media").glob("*.png")):
    im = Image.open(f)
    print(f.name, im.size)
