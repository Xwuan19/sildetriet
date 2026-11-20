"""Visual & Numerical Inspection of generated clean backgrounds."""

from PIL import Image
import numpy as np

def inspect_image(path):
    im = Image.open(path)
    w, h = im.size
    arr = np.array(im)
    
    print(f"=== File: {path.name} ===")
    print(f"Size: {w}x{h} (Aspect Ratio: {w/h:.3f}, expected 16:9 = {16/9:.3f})")
    print(f"Mode: {im.mode}")
    print(f"Channel min: R={arr[:,:,0].min()}, G={arr[:,:,1].min()}, B={arr[:,:,2].min()}")
    print(f"Channel max: R={arr[:,:,0].max()}, G={arr[:,:,1].max()}, B={arr[:,:,2].max()}")
    print(f"Channel mean: R={arr[:,:,0].mean():.1f}, G={arr[:,:,1].mean():.1f}, B={arr[:,:,2].mean():.1f}")
    
    # Check specific key zones:
    # 1. Focal zone (around cx=1410, cy=430)
    focal = arr[400:460, 1380:1440].mean(axis=(0,1))
    print(f"Focal aura sample (x=1410, y=430): RGB=({focal[0]:.1f}, {focal[1]:.1f}, {focal[2]:.1f})")
    
    # 2. Text reading area (Slide 1 title at x=400, y=300)
    title_area = arr[250:350, 350:450].mean(axis=(0,1))
    print(f"Text title backdrop sample (x=400, y=300): RGB=({title_area[0]:.1f}, {title_area[1]:.1f}, {title_area[2]:.1f})")
    
    # 3. Bottom left (x=100, y=950)
    bl = arr[900:1000, 50:150].mean(axis=(0,1))
    print(f"Bottom-left deep crimson sample: RGB=({bl[0]:.1f}, {bl[1]:.1f}, {bl[2]:.1f})")
    
    # 4. Bottom right (x=1800, y=1000)
    br = arr[950:1050, 1750:1850].mean(axis=(0,1))
    print(f"Bottom-right corner sample: RGB=({br[0]:.1f}, {br[1]:.1f}, {br[2]:.1f})")
    
    # Check for any abrupt edges or high frequency artifacts (gradient magnitude)
    arr_f = arr.astype(float)
    diff_x = np.abs(arr_f[:, 1:, :] - arr_f[:, :-1, :])
    diff_y = np.abs(arr_f[1:, :, :] - arr_f[:-1, :, :])
    max_gradient_x = diff_x.max()
    max_gradient_y = diff_y.max()
    mean_gradient_x = diff_x.mean()
    mean_gradient_y = diff_y.mean()
    print(f"Gradient smoothness: mean_diff_x={mean_gradient_x:.2f}, max_diff_x={max_gradient_x:.1f}")
    print(f"Gradient smoothness: mean_diff_y={mean_gradient_y:.2f}, max_diff_y={max_gradient_y:.1f}")
    print()

if __name__ == "__main__":
    from pathlib import Path
    inspect_image(Path("assets/master_stage_clean_bg.png"))
    inspect_image(Path("assets/stage_bg_clean_dimmed.png"))
