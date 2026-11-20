# -*- coding: utf-8 -*-
import json

with open("assets/models3d/lenin_seattle/Lenin_Seattle_Bronze.gltf", "r", encoding="utf-8") as f:
    d = json.load(f)

for i, m in enumerate(d.get("meshes", [])):
    p = m["primitives"][0]
    print(f"Mesh {i}: attributes={list(p.get('attributes', {}).keys())}, material={p.get('material')}")
    if i >= 3:
        break
