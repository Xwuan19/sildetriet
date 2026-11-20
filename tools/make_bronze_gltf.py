# -*- coding: utf-8 -*-
import json

gltf_file = r"assets\models3d\lenin_seattle\Lenin_Statue_@_Seattle.gltf"
with open(gltf_file, "r", encoding="utf-8") as f:
    d = json.load(f)

# Add bronze PBR material
d["materials"] = [
    {
        "name": "DarkBronzeStatue",
        "pbrMetallicRoughness": {
            "baseColorFactor": [0.35, 0.24, 0.15, 1.0], # Refined warm bronze patina
            "metallicFactor": 0.08,
            "roughnessFactor": 0.60
        },
        "doubleSided": True
    }
]

# Assign material 0 to all primitives in all meshes
for m in d.get("meshes", []):
    for p in m.get("primitives", []):
        p["material"] = 0

out_file = r"assets\models3d\lenin_seattle\Lenin_Seattle_Bronze.gltf"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(d, f)

print("Saved bronze glTF to:", out_file)
