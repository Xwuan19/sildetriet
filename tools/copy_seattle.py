# -*- coding: utf-8 -*-
import os
import shutil

src_dir = r"tools\sketchfab-cli\downloads\Lenin_Statue_@_Seattle-c31f674c"
dst_dir = r"assets\models3d\lenin_seattle"
os.makedirs(dst_dir, exist_ok=True)

for item in os.listdir(src_dir):
    s = os.path.join(src_dir, item)
    d = os.path.join(dst_dir, item)
    if os.path.isdir(s):
        shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        shutil.copy2(s, d)

print("Copied files to", dst_dir)
for f in os.listdir(dst_dir):
    print(" -", f)
