from PIL import Image
import glob

for p in sorted(glob.glob("preview_red/slideppt_media/*.png")):
    im = Image.open(p)
    print(f"{p}: size={im.size}, mode={im.mode}")
