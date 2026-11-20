import subprocess
import imageio_ffmpeg
from pathlib import Path

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = "preview_red/morph_preview.mp4"
out_dir = Path("preview_red/deck_morph_frames")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract from t=5.0s to t=8.5s at 10 fps (35 frames)
subprocess.run([
    ffmpeg, "-y",
    "-ss", "5.2",
    "-i", video,
    "-t", "3.0",
    "-vf", "fps=10",
    str(out_dir / "m_%03d.png")
], check=True)
print("Extracted deck morph frames!")
