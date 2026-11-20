# -*- coding: utf-8 -*-
obj_path = r"assets\models3d\lenin_seattle\Lenin_Seattle.obj"
with open(obj_path, "r", encoding="utf-8") as f:
    has_vt = False
    for i in range(100):
        line = f.readline()
        if line.startswith("vt "):
            has_vt = True
            break
print("Has vt in first 100 lines:", has_vt)

# Let's count vt
vt_count = 0
with open(obj_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("vt "):
            vt_count += 1
            if vt_count >= 10:
                break
print("VT count > 0:", vt_count > 0)
