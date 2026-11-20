# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json

query = '("lenin" OR "marx") AND (format:STL OR format:OBJ OR format:"3D Model" OR "3d scan" OR "bust")'
url = f"https://archive.org/advancedsearch.php?q={urllib.parse.quote(query)}&fl[]=identifier,title,mediatype,collection&rows=20&output=json"

headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"Total: {data['response']['numFound']}")
        for doc in data['response']['docs']:
            print(doc.get('identifier'), "|", doc.get('title'))
except Exception as e:
    print("Error:", e)
