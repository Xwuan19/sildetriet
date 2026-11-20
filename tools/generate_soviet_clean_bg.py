"""Production Generator for Soviet Constructivist Crimson Poster Backgrounds (1920x1080).
Creates:
  - assets/master_stage_clean_bg.png (1920x1080, 16:9, pure clean hero background)
  - assets/stage_bg_clean_dimmed.png (1920x1080, 16:9, dimmed variant for Slides 2 & 3)
"""

import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
PREVIEW = ROOT / "preview_red"
ASSETS.mkdir(exist_ok=True)
PREVIEW.mkdir(exist_ok=True)

W, H = 1920, 1080
CX, CY = 1411.0, 432.0  # Hero focal center (73.5% W, 40% H)

def smoothstep(edge0, edge1, x):
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def build_crimson_base():
    """
    Rich Soviet constructivist gradient canvas:
      Focal highlight aura: #C2282F (194, 40, 47)
      Ruby Crimson:        #8E191D (142, 25, 29)
      Rich Wine Red:       #650E13 (101, 14, 19)
      Deep Dark Crimson:   #2C0408 (44, 4, 8)
      Edge Vignette:       #180204 (24, 2, 4)
    """
    y, x = np.ogrid[:H, :W]
    
    # Distance from hero focal center with theatrical aspect ratio
    dx = (x - CX) / (W * 0.88)
    dy = (y - CY) / (H * 0.92)
    dist = np.sqrt(dx * dx + dy * dy)
    
    # Grounding bottom gradient (gives weight to the base of the presentation)
    y_bias = (y / float(H)) ** 1.35 * 0.45
    metric = dist + y_bias
    
    c_aura    = np.array([194.0, 40.0, 47.0])  # Radiant ruby focal glow
    c_ruby    = np.array([142.0, 25.0, 29.0])  # #8E191D
    c_wine    = np.array([101.0, 14.0, 19.0])  # #650E13
    c_dark    = np.array([44.0, 4.0, 8.0])     # #2C0408
    c_edge    = np.array([20.0, 2.0, 4.0])     # Edge boundary
    
    w0 = 1.0 - smoothstep(0.0, 0.28, metric)
    w1 = smoothstep(0.0, 0.28, metric) - smoothstep(0.28, 0.68, metric)
    w2 = smoothstep(0.28, 0.68, metric) - smoothstep(0.68, 1.22, metric)
    w3 = smoothstep(0.68, 1.22, metric) - smoothstep(1.22, 1.68, metric)
    w4 = smoothstep(1.22, 1.68, metric)
    
    base = (
        np.outer(w0, np.ones(3)).reshape(H, W, 3) * c_aura +
        np.outer(w1, np.ones(3)).reshape(H, W, 3) * c_ruby +
        np.outer(w2, np.ones(3)).reshape(H, W, 3) * c_wine +
        np.outer(w3, np.ones(3)).reshape(H, W, 3) * c_dark +
        np.outer(w4, np.ones(3)).reshape(H, W, 3) * c_edge
    )
    return base

def build_atmospheric_rays():
    """
    Subtle Soviet constructivist volumetric rays:
      Combines wide atmospheric light shafts with fine golden ray lines from assets/rays_gold.png.
    """
    y, x = np.ogrid[:H, :W]
    angles = np.arctan2(y - CY, x - CX)
    radii = np.sqrt((x - CX)**2 + (y - CY)**2)
    
    # 1. Soft atmospheric light beams (asymmetric harmonic angles)
    shaft1 = np.sin(angles * 9.0 + 0.3) * 0.5 + 0.5
    shaft2 = np.sin(angles * 17.0 - 0.5) * 0.5 + 0.5
    shafts = (shaft1 * 0.65 + shaft2 * 0.35) ** 1.8
    
    # Radial envelope: smooth fade near core, soft falloff at edges
    envelope = smoothstep(70.0, 320.0, radii) * (1.0 - smoothstep(800.0, 1850.0, radii) * 0.60)
    shaft_map = shafts * envelope
    
    # Gaussian blur for soft cinematic diffusion
    shaft_im = Image.fromarray((shaft_map * 255.0).clip(0, 255).astype(np.uint8))
    shaft_blur = shaft_im.filter(ImageFilter.GaussianBlur(16.0))
    shaft_smooth = np.array(shaft_blur, dtype=float) / 255.0
    
    # Color tint: ruby warmth (+18 R, +6 G)
    shaft_color = np.zeros((H, W, 3), dtype=float)
    shaft_color[:, :, 0] = shaft_smooth * 18.0
    shaft_color[:, :, 1] = shaft_smooth * 6.0
    shaft_color[:, :, 2] = shaft_smooth * 1.5
    
    # 2. Delicate golden fine rays from assets/rays_gold.png
    rays_asset_path = ASSETS / "rays_gold.png"
    if rays_asset_path.exists():
        im_gold_rays = Image.open(rays_asset_path).convert("RGBA")
        im_gold_rays = im_gold_rays.resize((W, H), Image.LANCZOS)
        arr_gold = np.array(im_gold_rays, dtype=float)
        # Soften ray center (avoid pinpoint convergence dot at CX, CY)
        center_soften = smoothstep(12.0, 95.0, radii)
        # Gold rays alpha mask (boosted slightly for visible golden shimmer)
        gold_alpha = (arr_gold[:, :, 3] / 255.0) * 2.6 * center_soften
        gold_rgb = arr_gold[:, :, :3]
        gold_layer = gold_rgb * gold_alpha[:, :, np.newaxis]
    else:
        gold_layer = np.zeros((H, W, 3), dtype=float)
        
    return shaft_color + gold_layer

def blend_clean_flag_drape(canvas):
    """
    Incorporates the authentic Soviet red silk curtain fold from assets/master_stage_bg.png,
    with any video artifacts / watermarks thoroughly cleaned and harmonized.
    """
    src_path = ASSETS / "master_stage_bg.png"
    if not src_path.exists():
        return canvas
        
    im_src = Image.open(src_path).convert("RGB")
    arr_src = np.array(im_src, dtype=float)
    
    drape_w = 340
    drape_h = 860
    drape = arr_src[:drape_h, :drape_w, :].copy()
    
    # Clean the video frame artifact at y=715..755, x=15..85
    clean_patch = drape[670:700, :100, :].mean(axis=(0, 1))
    for yy in range(710, 760):
        for xx in range(10, 90):
            drape[yy, xx, :] = clean_patch
            
    # Clean any stray bright video speckles in the entire drape region
    # The fabric is deep crimson (R: 120-220, G: 0-45, B: 0-45)
    # Any pixel with G > 50 or B > 50 or (R > 210 and G > 35) is a speckle
    speckle_mask = (drape[:, :, 1] > 48) | (drape[:, :, 2] > 48)
    # Median / neighbor replacement for speckles
    for c in range(3):
        ch = drape[:, :, c]
        # Replace speckle pixels with local mean
        ch[speckle_mask] = clean_patch[c]
        drape[:, :, c] = ch
        
    # Smooth the drape to give luxurious silky satin feel and remove compression noise
    im_drape = Image.fromarray(np.clip(drape, 0, 255).astype(np.uint8))
    im_drape_clean = im_drape.filter(ImageFilter.GaussianBlur(1.1))
    drape_clean = np.array(im_drape_clean, dtype=float)
    
    # Blend mask: seamlessly feather out to the right and bottom
    yd, xd = np.ogrid[:drape_h, :drape_w]
    alpha_x = 1.0 - smoothstep(drape_w * 0.40, drape_w * 0.96, xd)
    alpha_y = 1.0 - smoothstep(drape_h * 0.65, drape_h * 0.98, yd)
    blend_mask = (alpha_x * alpha_y)[:, :, np.newaxis]
    
    # Color match: harmonize drape highlights to deep crimson palette
    drape_harmonized = drape_clean * 0.90 + np.array([12.0, 1.0, 2.0]) * 0.10
    
    canvas[:drape_h, :drape_w, :] = (
        drape_harmonized * blend_mask + canvas[:drape_h, :drape_w, :] * (1.0 - blend_mask)
    )
    return canvas

def apply_vintage_grain(canvas, strength=0.032):
    """
    Fine vintage lithographic paper grain for authentic 1920s poster feel.
    """
    np.random.seed(1917)
    noise = np.random.normal(0.0, 1.0, (H, W))
    im_noise = Image.fromarray(((noise + 3.0) / 6.0 * 255.0).clip(0, 255).astype(np.uint8))
    im_noise_smooth = im_noise.filter(ImageFilter.GaussianBlur(0.5))
    noise_factor = (np.array(im_noise_smooth, dtype=float) / 255.0 - 0.5) * strength
    return canvas * (1.0 + noise_factor[:, :, np.newaxis])

def apply_frame_vignette(canvas):
    """
    Subtle vignette around the outer borders to anchor the 16:9 frame.
    """
    y, x = np.ogrid[:H, :W]
    edge_x = np.minimum(x, W - 1 - x) / (W * 0.12)
    edge_y = np.minimum(y, H - 1 - y) / (H * 0.12)
    edge_val = np.clip(np.minimum(edge_x, edge_y), 0.0, 1.0)
    vignette = 0.92 + 0.08 * smoothstep(0.0, 1.0, edge_val)
    return canvas * vignette[:, :, np.newaxis]

def generate_all():
    print("Generating master_stage_clean_bg.png...")
    base = build_crimson_base()
    rays = build_atmospheric_rays()
    canvas = base + rays
    canvas = blend_clean_flag_drape(canvas)
    canvas = apply_vintage_grain(canvas, strength=0.032)
    canvas = apply_frame_vignette(canvas)
    
    master_arr = np.clip(canvas, 0, 255).astype(np.uint8)
    im_master = Image.fromarray(master_arr)
    
    master_path = ASSETS / "master_stage_clean_bg.png"
    im_master.save(master_path, quality=98)
    im_master.save(PREVIEW / "master_stage_clean_bg_preview.png")
    print(f"  -> Saved {master_path} ({W}x{H})")
    
    # Generate dimmed version for Slide 2 & 3
    print("Generating stage_bg_clean_dimmed.png...")
    # Shift towards deeper velvety wine/charcoal crimson, optimize text contrast
    dimmed_arr = canvas.copy()
    dimmed_arr = dimmed_arr * 0.70 + np.array([22.0, 3.0, 5.0]) * 0.30
    
    # Extra shadow in the left card reading zone (x < 1250)
    y, x = np.ogrid[:H, :W]
    card_zone = (1.0 - smoothstep(300.0, 1300.0, x)) * 0.15
    dimmed_arr = dimmed_arr * (1.0 - card_zone[:, :, np.newaxis])
    
    im_dimmed = Image.fromarray(np.clip(dimmed_arr, 0, 255).astype(np.uint8))
    dimmed_path = ASSETS / "stage_bg_clean_dimmed.png"
    im_dimmed.save(dimmed_path, quality=98)
    im_dimmed.save(PREVIEW / "stage_bg_clean_dimmed_preview.png")
    print(f"  -> Saved {dimmed_path} ({W}x{H})")
    
    return im_master, im_dimmed

if __name__ == "__main__":
    generate_all()
