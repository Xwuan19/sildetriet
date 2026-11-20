from PIL import Image, ImageDraw
from pathlib import Path

frames_dir = Path("preview_red/video_first_6s")
frames = sorted(list(frames_dir.glob("f_*.png")))

sheet = Image.new("RGB", (6 * 320, 4 * 180), color=(20, 20, 20))
draw = ImageDraw.Draw(sheet)

for i, f_path in enumerate(frames[:24]):
    im = Image.open(f_path).resize((320, 180))
    r = i // 6
    c = i % 6
    x = c * 320
    y = r * 180
    sheet.paste(im, (x, y))
    
    t_sec = i * 0.25
    txt = f"#{i+1} | {t_sec:.2f}s"
    draw.rectangle([x + 4, y + 4, x + 90, y + 24], fill=(0, 0, 0, 200))
    draw.text((x + 8, y + 6), txt, fill=(255, 230, 100))

sheet.save("preview_red/first_6s_sheet.png")
print("Saved first_6s_sheet.png")
