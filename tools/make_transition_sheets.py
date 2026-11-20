# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.load_default()

def make_sheet(folder, out_file, cols=4, thumb_w=360, thumb_h=202):
    frames = sorted(Path(folder).glob("*.jpg"))
    if not frames:
        return
    rows = (len(frames) + cols - 1) // cols
    pad = 8
    sw = cols * (thumb_w + pad) + pad
    sh = rows * (thumb_h + pad + 18) + pad
    sheet = Image.new("RGB", (sw, sh), (20, 20, 20))
    draw = ImageDraw.Draw(sheet)
    for i, f in enumerate(frames):
        r, c = i // cols, i % cols
        x = pad + c * (thumb_w + pad)
        y = pad + r * (thumb_h + pad + 18)
        im = Image.open(f).resize((thumb_w, thumb_h), Image.LANCZOS)
        sheet.paste(im, (x, y))
        draw.text((x + 4, y + thumb_h + 2), f.name, fill=(240, 240, 240), font=font)
    sheet.save(out_file, quality=90)
    print("Saved", out_file)

make_sheet("video_analysis/transition_1_2", "video_analysis/transition_1_2_sheet.jpg", cols=4)
make_sheet("video_analysis/transition_2_3", "video_analysis/transition_2_3_sheet.jpg", cols=4)
make_sheet("video_analysis/transition_end", "video_analysis/transition_end_sheet.jpg", cols=4)
