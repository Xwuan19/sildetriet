import subprocess
from pathlib import Path
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
mp4 = "preview_red/morph_preview.mp4"
out_dir = Path("preview_red/morph_frames")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract frames at 10 fps
cmd = [
    ffmpeg, "-y",
    "-i", mp4,
    "-vf", "fps=5",
    str(out_dir / "frame_%03d.png")
]
subprocess.run(cmd, check=True)
print("Extracted frames!")
