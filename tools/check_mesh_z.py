# -*- coding: utf-8 -*-
import json
import struct

with open("assets/models3d/lenin_seattle/Lenin_Statue_@_Seattle.gltf", "r", encoding="utf-8") as f:
    d = json.load(f)

bin_file = "assets/models3d/lenin_seattle/" + d["buffers"][0]["uri"]
with open(bin_file, "rb") as bf:
    bin_data = bf.read()

# Let's inspect mesh 0..15 min and max Z coordinates
for i, m in enumerate(d.get("meshes", [])):
    p = m["primitives"][0]
    pos_acc = d["accessors"][p["attributes"]["POSITION"]]
    bv = d["bufferViews"][pos_acc["bufferView"]]
    offset = bv.get("byteOffset", 0) + pos_acc.get("byteOffset", 0)
    count = pos_acc["count"]
    # read vertices
    # check min Z and max Z
    min_z = pos_acc["min"][2]
    max_z = pos_acc["max"][2]
    print(f"Mesh {i:2d}: count={count:5d}, Z range: [{min_z:.2f}, {max_z:.2f}]")
