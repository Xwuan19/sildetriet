# -*- coding: utf-8 -*-
"""Làm sạch silhouette Lenin và tạo lại phiên bản warm/gold."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SRC = ASSETS / "lenin_cutout.png"


def colorize(gray, stops):
    stops = sorted(stops)
    def lut(idx):
        out = []
        for i in range(256):
            t = i / 255
            if t <= stops[0][0]:
                out.append(stops[0][1][idx])
                continue
            if t >= stops[-1][0]:
                out.append(stops[-1][1][idx])
                continue
            for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
                if p0 <= t <= p1:
                    k = (t - p0) / max(1e-6, p1 - p0)
                    out.append(round(c0[idx] + (c1[idx] - c0[idx]) * k))
                    break
        return out
    return Image.merge("RGB", (gray.point(lut(0)), gray.point(lut(1)), gray.point(lut(2))))


def clean_alpha(im):
    alpha = np.array(im.getchannel("A"))
    mask = alpha > 24

    # giữ thành phần lớn nhất (bỏ mảng nền/ghế rời)
    labels, count = ndimage.label(mask)
    if count > 1:
        sizes = ndimage.sum(mask, labels, range(1, count + 1))
        mask = labels == (1 + int(np.argmax(sizes)))
        print(f"  bỏ {count - 1} mảnh rời")

    # đóng các lỗ nhỏ, mở để cắt cầu nối mảnh
    mask = ndimage.binary_closing(mask, structure=np.ones((5, 5)), iterations=2)
    mask = ndimage.binary_opening(mask, structure=np.ones((3, 3)), iterations=2)

    soft = ndimage.gaussian_filter(mask.astype(np.float32), 1.6)
    soft = np.clip(soft * 255 * 1.08, 0, 255).astype(np.uint8)
    im.putalpha(Image.fromarray(soft))
    return im


def with_glow(im, color=(210, 160, 78), strength=0.20, blur=7):
    pad = 24
    canvas = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    edge = im.getchannel("A").filter(ImageFilter.GaussianBlur(blur))
    edge = edge.point(lambda v: int(v * strength))
    alpha = Image.new("L", canvas.size, 0)
    alpha.paste(edge, (pad, pad))
    glow = Image.new("RGBA", canvas.size, color + (0,))
    glow.putalpha(alpha)
    canvas.alpha_composite(glow)
    canvas.alpha_composite(im, (pad, pad))
    return canvas


def checker(im):
    tile = 24
    bg = Image.new("RGB", im.size, (210, 210, 210))
    px = bg.load()
    for y in range(0, im.height, tile):
        for x in range(0, im.width, tile):
            if (x // tile + y // tile) % 2:
                for yy in range(y, min(y + tile, im.height)):
                    for xx in range(x, min(x + tile, im.width)):
                        px[xx, yy] = (170, 170, 170)
    bg = bg.convert("RGBA")
    bg.alpha_composite(im)
    return bg


def main():
    im = Image.open(SRC).convert("RGBA")
    print(f"nguồn: {im.size}")
    im = clean_alpha(im)
    # bỏ phần đáy còn ghế/tay
    im = im.crop((0, 0, im.width, im.height - 90))
    bbox = im.getchannel("A").getbbox()
    if bbox:
        im = im.crop((max(0, bbox[0] - 6), max(0, bbox[1] - 6),
                      min(im.width, bbox[2] + 6), min(im.height, bbox[3] + 6)))
    print(f"làm sạch: {im.size}")
    im.save(ASSETS / "lenin_cutout_clean.png")

    from PIL import ImageOps
    gray = ImageOps.autocontrast(im.convert("RGB").convert("L"), cutoff=0.5)

    warm = colorize(gray, [
        (0.00, (16, 2, 3)),
        (0.22, (62, 16, 18)),
        (0.50, (118, 76, 66)),
        (0.76, (186, 150, 122)),
        (1.00, (250, 240, 222)),
    ])
    warm.putalpha(im.getchannel("A"))
    hero = with_glow(warm, strength=0.20, blur=7)
    hero.save(ASSETS / "lenin_warm.png")
    checker(hero).resize((hero.width // 3, hero.height // 3)).save(ASSETS / "lenin_preview.png")

    gold = colorize(gray, [
        (0.00, (20, 2, 3)),
        (0.18, (58, 7, 10)),
        (0.40, (112, 18, 19)),
        (0.60, (160, 70, 36)),
        (0.79, (212, 160, 88)),
        (1.00, (255, 244, 210)),
    ])
    gold.putalpha(im.getchannel("A"))
    gold.save(ASSETS / "lenin_gold.png")
    print("xong")


if __name__ == "__main__":
    main()
