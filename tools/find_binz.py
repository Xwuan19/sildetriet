# -*- coding: utf-8 -*-
with open("tools/find_sf_links.py", "r", encoding="utf-8") as f:
    pass

import urllib.request
import re

url = "https://sketchfab.com/3d-models/lenin-statue-seattle-c31f674c90b14cb194244b456bb8cf06"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode("utf-8")

idx = html.find("file.binz")
if idx != -1:
    print(html[idx-300:idx+300])
