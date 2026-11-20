import subprocess
import imageio_ffmpeg
from pathlib import Path
from PIL import Image, ImageDraw

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
out_dir = Path("preview_red/exact_p2_50fps")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract from 7.7s to 9.7s (100 frames at 50fps = 20ms each)
subprocess.run([
    ffmpeg, "-y",
    "-ss", "7.7",
    "-i", video,
    "-t", "2.0",
    "-vf", "fps=50",
    str(out_dir / "frame_%04d.png")
], check=True)

frames = sorted(list(out_dir.glob("frame_*.png")))
print(f"Extracted {len(frames)} frames from 7.7s!")

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
            
            t_ms = 7700 + frame_idx * 20
            txt = f"#{frame_idx+1:03d} | {t_ms}ms"
            draw.rectangle([x + 6, y + 6, x + 120, y + 26], fill=(0, 0, 0, 200))
            draw.text((x + 10, y + 8), txt, fill=(255, 230, 100))
            
    sheet.save(f"preview_red/p2_50fps_sheet_{sheet_idx}.png")
    print(f"Saved p2 sheet {sheet_idx}")
