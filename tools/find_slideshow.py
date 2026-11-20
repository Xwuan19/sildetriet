from pathlib import Path
from PIL import Image
import numpy as np

# Find where the PowerPoint UI disappears and full-screen slideshow starts!
sec_dir = Path("preview_red/all_seconds")
secs = sorted(list(sec_dir.glob("sec_*.png")))

for i, s in enumerate(secs):
    im = Image.open(s)
    # Check top-left corner (in PPT UI it's title bar/menu, in slideshow it's slide content)
    top_strip = np.array(im.crop((0, 0, 1920, 50)))
    # PPT UI top strip has gray/red Ribbon
    # Fullscreen slide has slide background
    print(f"sec_{i+1:03d}: mean color top strip = {np.mean(top_strip, axis=(0,1))[:3]}")
