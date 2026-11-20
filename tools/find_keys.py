# -*- coding: utf-8 -*-
import re
with open("assets/models3d/lenin_seattle/file.osgjs", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

keys = set(re.findall(r'"([A-Za-z0-9_]+)":\s*\{\s*"UniqueID":\s*\d+,\s*"Array":', text))
print("Array keys in file.osgjs:", keys)
