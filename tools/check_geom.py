# -*- coding: utf-8 -*-
with open("assets/models3d/lenin_seattle/file.osgjs", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read(10000)
import json
data = json.loads(text[:text.rfind('}')+1]) if False else None
# let's grep for VertexAttributeList
import re
print("Matches for VertexAttributeList:")
for m in re.finditer(r'"VertexAttributeList"\s*:\s*\{([^}]+)\}', text):
    print(m.group(0)[:300])
