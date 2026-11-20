# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json

base = "https://commons.wikimedia.org/w/api.php"
params = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": "lenin .stl",
    "srnamespace": "6", # File: namespace
    "srlimit": "20"
}
url = base + "?" + urllib.parse.urlencode(params)
headers = {"User-Agent": "MyBot/1.0 (test@example.com)"}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(json.dumps(data, indent=2))
except Exception as e:
    print("Error:", e)
