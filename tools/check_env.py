# -*- coding: utf-8 -*-
import os
import subprocess
import sys

print("Python executable:", sys.executable)
try:
    import imageio
    print("imageio available")
except ImportError:
    print("imageio not installed")

# Try to check if pip can install opencv-python-headless or if ffmpeg is in some common path
res = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
print("Pip list sample:\n" + "\n".join(res.stdout.splitlines()[:20]))
