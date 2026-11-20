# -*- coding: utf-8 -*-
import urllib.request
import re
import json

url = "https://sketchfab.com/3d-models/lenin-statue-seattle-c31f674c90b14cb194244b456bb8cf06"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8")
        print("HTML length:", len(html))
        # Look for model urls, .bin, .gltf, etc.
        matches = re.findall(r'https://[^"\'\s]+\.(?:bin|gltf|glb|zip|osgjs)', html)
        print("Matches:", set(matches))
        
        # Check for window.preloaded
        m_pre = re.search(r'window\.preloaded\s*=\s*(\{.*?\});', html)
        if m_pre:
            print("Found preloaded data!")
            # let's save to file
            with open("preview_red/preloaded.json", "w", encoding="utf-8") as f:
                f.write(m_pre.group(1))
except Exception as e:
    print("Error:", e)
