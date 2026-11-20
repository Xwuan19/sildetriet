# -*- coding: utf-8 -*-
import urllib.request
import json

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://www.thingiverse.com/thing:286624/zip"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print("Status:", resp.status)
        print("Content-Type:", resp.headers.get("Content-Type"))
        print("Length:", len(resp.read(1024)))
except Exception as e:
    print("Error:", e)
