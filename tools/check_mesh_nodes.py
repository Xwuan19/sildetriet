# -*- coding: utf-8 -*-
import json
import struct

gltf_file = r"assets\models3d\lenin_seattle\Lenin_Seattle_Bronze.gltf"
with open(gltf_file, "r", encoding="utf-8") as f:
    d = json.load(f)

print("Nodes count:", len(d.get("nodes", [])))
for i, n in enumerate(d.get("nodes", [])):
    print(f"Node {i}: {n.get('name')}, mesh={n.get('mesh')}, translation={n.get('translation')}, scale={n.get('scale')}")

print("Meshes count:", len(d.get("meshes", [])))
for i, m in enumerate(d.get("meshes", [])):
    print(f"Mesh {i}: {m.get('name')}, prims={len(m.get('primitives', []))}")
