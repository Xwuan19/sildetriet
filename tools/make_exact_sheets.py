from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

frames_dir = Path("preview_red/exact_ref_50fps")
frames = sorted(list(frames_dir.glob("frame_*.png")))

# Let's create contact sheets of 20 frames each (5 cols x 4 rows)
# 100 frames total -> 5 sheets of 20 frames = 400ms per sheet!
for sheet_idx in range(5):
    sheet = Image.new("RGB", (5 * 384, 4 * 216), color=(20, 20, 20))
    draw = ImageDraw.Draw(sheet)
    for i in range(20):
        frame_idx = sheet_idx * 20 + i
        if frame_idx < len(frames):
            f_path = frames[frame_idx]
            im = Image.open(f_path).resize((384, 216))
            r = i // 5
            c = i % 5
            x = c * 384
            y = r * 216
            sheet.paste(im, (x, y))
            
            # Draw timestamp badge
            ms = frame_idx * 20
            txt = f"#{frame_idx+1:03d} | {ms}ms"
            draw.rectangle([x + 6, y + 6, x + 110, y + 26], fill=(0, 0, 0, 200))
            draw.text((x + 10, y + 8), txt, fill=(255, 230, 100))
            
    sheet.save(f"preview_red/ref_50fps_sheet_{sheet_idx}.png")
    print(f"Saved sheet {sheet_idx} (frames {sheet_idx*20+1} to {(sheet_idx+1)*20})")
