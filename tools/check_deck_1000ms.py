import subprocess
import imageio_ffmpeg
from pathlib import Path
from PIL import Image, ImageDraw

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = "preview_red/morph_preview.mp4"
out_dir = Path("preview_red/deck_morph_1000ms")
out_dir.mkdir(parents=True, exist_ok=True)

# Transition 1 from Slide 1 to Slide 2 is around 5.0s to 7.0s
subprocess.run([
    ffmpeg, "-y",
    "-ss", "5.0",
    "-i", video,
    "-t", "2.0",
    "-vf", "fps=50",
    str(out_dir / "m_%04d.png")
], check=True)

frames = sorted(list(out_dir.glob("m_*.png")))
print(f"Extracted {len(frames)} frames at 50fps from deck video!")

sheet = Image.new("RGB", (5 * 384, 4 * 216), color=(20, 20, 20))
draw = ImageDraw.Draw(sheet)
# Take 20 frames spaced evenly across the 1000ms transition
for i in range(20):
    idx = int(i * (len(frames) / 20))
    if idx < len(frames):
        im = Image.open(frames[idx]).resize((384, 216))
        r = i // 5
        c = i % 5
        x = c * 384
        y = r * 216
        sheet.paste(im, (x, y))
        ms = idx * 20
        txt = f"+{ms}ms"
        draw.rectangle([x + 6, y + 6, x + 80, y + 26], fill=(0, 0, 0, 200))
        draw.text((x + 10, y + 8), txt, fill=(255, 230, 100))

sheet.save("preview_red/deck_morph_1000ms_sheet.png")
print("Saved deck_morph_1000ms_sheet.png")
