# -*- coding: utf-8 -*-
import json

gltf_file = r"assets\models3d\lenin_seattle\Lenin_Seattle_Bronze.gltf"
with open(gltf_file, "r", encoding="utf-8") as f:
    d = json.load(f)

for i, m in enumerate(d.get("meshes", [])):
    p = m["primitives"][0]
    pos_acc_id = p["attributes"]["POSITION"]
    acc = d["accessors"][pos_acc_id]
    min_v = [round(x, 2) for x in acc.get("min", [])]
    max_v = [round(x, 2) for x in acc.get("max", [])]
    print(f"Mesh {i:2d}: count={acc.get('count'):5d}, min={min_v}, max={max_v}")
