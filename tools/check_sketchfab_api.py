# -*- coding: utf-8 -*-
import urllib.request
import json

url = "https://api.sketchfab.com/v3/models/c31f674c90b14cb194244b456bb8cf06"
headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print("Name:", data.get("name"))
        print("isDownloadable:", data.get("isDownloadable"))
        print("archives:", data.get("archives"))
        print("files:", data.get("files"))
except Exception as e:
    print("Error:", e)
