# -*- coding: utf-8 -*-
import glob, os
from PIL import Image
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
frames = sorted(glob.glob(r'C:\Users\ADMIN\Downloads\sildetriet\preview_red\sample_frames\frame_*.jpg'))
for f in frames:
    im = Image.open(f).convert('RGB')
    w,h = im.size
    px = im.resize((64,36))
    data = list(px.getdata())
    def av(ps): return tuple(sum(p[i] for p in ps)//len(ps) for i in range(3))
    left = [data[y*64+x] for y in range(36) for x in range(32)]
    right = [data[y*64+x] for y in range(36) for x in range(32,64)]
    top = data[:64*18]
    bot = data[64*18:]
    # brightness variance as rough "activity"
    lum = [0.299*r+0.587*g+0.114*b for r,g,b in data]
    mean = sum(lum)/len(lum)
    var = sum((x-mean)**2 for x in lum)/len(lum)
    print(f"{os.path.basename(f)} L={av(left)} R={av(right)} T={av(top)} B={av(bot)} var={int(var)}")
