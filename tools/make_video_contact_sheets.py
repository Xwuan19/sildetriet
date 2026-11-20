# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

frames_dir = Path("video_analysis/frames")
frames = sorted(frames_dir.glob("frame_*.jpg"))

out_dir = Path("video_analysis/contact_sheets")
out_dir.mkdir(parents=True, exist_ok=True)

# Grid: 5 columns x 6 rows = 30 frames per sheet
cols = 5
rows = 6
thumb_w = 320
thumb_h = 180
pad = 10
font = ImageFont.load_default()

for sheet_idx in range(4):
    start = sheet_idx * 30
    end = min(len(frames), start + 30)
    batch = frames[start:end]
    if not batch:
        break
    
    sheet_w = cols * (thumb_w + pad) + pad
    sheet_h = rows * (thumb_h + pad + 20) + pad
    sheet = Image.new("RGB", (sheet_w, sheet_h), (25, 25, 25))
    draw = ImageDraw.Draw(sheet)
    
    for i, f in enumerate(batch):
        r = i // cols
        c = i % cols
        x = pad + c * (thumb_w + pad)
        y = pad + r * (thumb_h + pad + 20)
        
        im = Image.open(f).resize((thumb_w, thumb_h), Image.LANCZOS)
        sheet.paste(im, (x, y))
        
        f_num = start + i + 1
        t_sec = (f_num - 1) * 0.5
        label = f"#{f_num:03d} ({t_sec:.1f}s)"
        draw.text((x + 4, y + thumb_h + 2), label, fill=(220, 220, 220), font=font)
        
    out_path = out_dir / f"sheet_{sheet_idx + 1}.jpg"
    sheet.save(out_path, quality=85)
    print("Saved", out_path)
