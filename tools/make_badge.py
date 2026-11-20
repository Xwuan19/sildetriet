# -*- coding: utf-8 -*-
"""Dựng huy hiệu tròn: đĩa đỏ sâu + viền vàng + chân dung Lenin đã xử lý vàng."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SRC = ASSETS / "lenin_medallion.png"
OUT = ASSETS / "lenin_badge.png"

SIZE = 1200


def radial_disk(size: int) -> Image.Image:
    """Đĩa đỏ có gradient xuyên tâm, sáng nhẹ phía sau đầu."""
    y, x = np.mgrid[0:size, 0:size].astype(np.float32)
    cx, cy = size * 0.5, size * 0.44
    r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / (size * 0.62)
    r = np.clip(r, 0, 1)
    # hai màu: tâm ấm, rìa gần đen đỏ
    inner = np.array([126, 22, 26], dtype=np.float32)
    outer = np.array([40, 4, 7], dtype=np.float32)
    k = (r ** 1.15)[..., None]
    rgb = inner * (1 - k) + outer * k
    alpha = np.full((size, size), 255, dtype=np.uint8)
    return Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8), "RGBA")


def main() -> None:
    disk = radial_disk(SIZE)

    # viền vàng ngoài + quầng mảnh
    rim = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(rim)
    d.ellipse((8, 8, SIZE - 9, SIZE - 9), outline=(214, 175, 100, 255), width=5)
    d.ellipse((24, 24, SIZE - 25, SIZE - 25), outline=(244, 223, 163, 70), width=2)
    glow = rim.filter(ImageFilter.GaussianBlur(10))
    glow.putalpha(glow.getchannel("A").point(lambda v: int(v * 0.55)))

    # cắt đĩa theo hình tròn
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse((8, 8, SIZE - 9, SIZE - 9), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.8))
    disk.putalpha(ImageChops.multiply(disk.getchannel("A"), mask))

    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.alpha_composite(glow)
    canvas.alpha_composite(disk)
    canvas.alpha_composite(rim)

    portrait = Image.open(SRC).convert("RGBA")
    if portrait.size != (SIZE, SIZE):
        portrait = portrait.resize((SIZE, SIZE), Image.LANCZOS)
    # đẩy chân dung xuống để đỉnh đầu có khoảng thở; mép vuông dưới bị viền tròn cắt
    shifted = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shifted.alpha_composite(portrait, (0, 46))
    # cắt chân dung đúng trong lòng huy hiệu
    inner_mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(inner_mask).ellipse((14, 14, SIZE - 15, SIZE - 15), fill=255)
    inner_mask = inner_mask.filter(ImageFilter.GaussianBlur(1.2))
    shifted.putalpha(ImageChops.multiply(shifted.getchannel("A"), inner_mask))
    canvas.alpha_composite(shifted)

    # vignette nhẹ để mép chân dung chìm vào đĩa
    vignette = Image.new("L", (SIZE, SIZE), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-90, -90, SIZE + 90, SIZE + 90), fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(120))
    shade = Image.new("RGBA", (SIZE, SIZE), (31, 3, 5, 0))
    shade_alpha = ImageChops.invert(vignette).point(lambda v: int(v * 0.55))
    # chỉ làm tối trong lòng huy hiệu, không để lại nền vuông ở bốn góc
    shade_alpha = ImageChops.multiply(shade_alpha, mask)
    shade.putalpha(shade_alpha)
    canvas.alpha_composite(shade)

    canvas.save(OUT)
    print(f"đã lưu {OUT.name} {canvas.size}")


if __name__ == "__main__":
    main()
