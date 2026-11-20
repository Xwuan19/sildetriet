# -*- coding: utf-8 -*-
"""
Chuẩn bị ảnh Lenin cho deck đỏ – vàng:
  - tách nền bằng rembg (u2net)
  - cắt bỏ ghế/tay ở đáy, giữ chân dung nửa người
  - hai phiên bản màu: warm (da ấm) và gold (poster vàng – đỏ)
  - medallion tròn cho slide giới thiệu nhóm
  - tia sáng vàng + grain cho nền
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps
from rembg import new_session, remove

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SRC = ASSETS / "lenin_1920.jpg"


def colorize(gray: Image.Image, stops: list[tuple[float, tuple[int, int, int]]]) -> Image.Image:
    """Ánh xạ độ sáng 0..255 qua các stop màu."""
    stops = sorted(stops, key=lambda s: s[0])

    def lut_channel(idx: int) -> list[int]:
        out = []
        for i in range(256):
            t = i / 255.0
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

    r = gray.point(lut_channel(0))
    g = gray.point(lut_channel(1))
    b = gray.point(lut_channel(2))
    return Image.merge("RGB", (r, g, b))


def trim(im: Image.Image, pad: int = 8) -> Image.Image:
    bbox = im.getchannel("A").getbbox()
    if not bbox:
        return im
    l, t, r, b = bbox
    return im.crop((max(0, l - pad), max(0, t - pad),
                    min(im.width, r + pad), min(im.height, b + pad)))


def cutout(im: Image.Image, session) -> Image.Image:
    rgba = remove(im, session=session, alpha_matting=False)
    alpha = rgba.getchannel("A")
    alpha = alpha.point(lambda v: 0 if v < 10 else (255 if v > 245 else v))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    rgba.putalpha(alpha)
    return rgba


def with_glow(im: Image.Image, color=(228, 188, 104), strength=0.42, blur=8) -> Image.Image:
    pad = 26
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


def circular(im: Image.Image, size: int = 1200) -> Image.Image:
    im = ImageOps.fit(im, (size, size), Image.LANCZOS, centering=(0.5, 0.35))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((3, 3, size - 4, size - 4), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.6))
    im.putalpha(ImageChops.multiply(im.getchannel("A"), mask))
    return im


def make_rays(path: Path, w: int = 2400, h: int = 1350) -> None:
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    cx, cy = int(w * 0.735), int(h * 0.40)
    length = int(w * 0.75)
    import math
    for i in range(72):
        ang = (i / 72) * math.tau
        a = 10 if i % 2 == 0 else 5
        width = 3 if i % 3 == 0 else 1
        x2 = cx + math.cos(ang) * length
        y2 = cy + math.sin(ang) * length
        draw.line([(cx, cy), (x2, y2)], fill=(238, 201, 118, a), width=width)
    layer = layer.filter(ImageFilter.GaussianBlur(1.4))
    layer.save(path)
    print(f"  tia sáng: {path.name}")


def make_grain(path: Path, w: int = 2000, h: int = 1125) -> None:
    noise = Image.effect_noise((w, h), 26).filter(ImageFilter.GaussianBlur(0.6)).convert("L")
    alpha = noise.point(lambda v: int(((v / 255.0) ** 2) * 24))
    grain = Image.new("RGBA", (w, h), (34, 4, 6, 0))
    grain.putalpha(alpha)
    grain.save(path)
    print(f"  grain: {path.name}")


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Thiếu ảnh: {SRC}")
    print("Đang tải model tách nền (lần đầu có thể lâu)…")
    session = new_session("u2net")

    im = Image.open(SRC).convert("RGB")
    # bỏ ghế + bàn tay ở đáy, giữ đầu → ngực/eo
    im = im.crop((250, 0, 1990, 2470))
    im.thumbnail((1500, 2200), Image.LANCZOS)
    print(f"Ảnh làm việc: {im.size}")

    cut = cutout(im, session)
    cut = trim(cut, pad=6)
    cut.save(ASSETS / "lenin_cutout.png")
    print(f"  cutout: {cut.size}")

    gray = ImageOps.autocontrast(cut.convert("RGB").convert("L"), cutoff=0.5)
    alpha = cut.getchannel("A")

    warm = colorize(gray, [
        (0.00, (16, 2, 3)),
        (0.22, (62, 16, 18)),
        (0.50, (118, 76, 66)),
        (0.76, (186, 150, 122)),
        (1.00, (250, 240, 222)),
    ])
    warm.putalpha(alpha)
    with_glow(warm).save(ASSETS / "lenin_warm.png")
    print("  lenin_warm.png")

    gold = colorize(gray, [
        (0.00, (20, 2, 3)),
        (0.18, (58, 7, 10)),
        (0.40, (112, 18, 19)),
        (0.60, (160, 70, 36)),
        (0.79, (212, 160, 88)),
        (1.00, (255, 244, 210)),
    ])
    gold.putalpha(alpha)
    gold.save(ASSETS / "lenin_gold.png")
    print("  lenin_gold.png")

    # medallion: tách nền riêng trên crop đầu – vai để crop tròn đẹp
    head = Image.open(SRC).convert("RGB").crop((300, 0, 1770, 1470))
    head.thumbnail((1400, 1400), Image.LANCZOS)
    head_cut = cutout(head, session)
    head_gray = ImageOps.autocontrast(head_cut.convert("RGB").convert("L"), cutoff=0.5)
    head_gold = colorize(head_gray, [
        (0.00, (24, 3, 4)),
        (0.25, (74, 10, 13)),
        (0.52, (140, 42, 32)),
        (0.76, (208, 152, 82)),
        (1.00, (255, 246, 218)),
    ])
    head_gold.putalpha(head_cut.getchannel("A"))
    circular(head_gold, 1200).save(ASSETS / "lenin_medallion.png")
    print("  lenin_medallion.png")

    make_rays(ASSETS / "rays_gold.png")
    make_grain(ASSETS / "grain_red.png")


if __name__ == "__main__":
    main()
