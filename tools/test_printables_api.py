# -*- coding: utf-8 -*-
import urllib.request
import json

url = "https://api.printables.com/graphql/"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}
query = {
    "query": """
    query GetPrint($id: ID!) {
        print(id: $id) {
            id
            name
            files {
                id
                name
                filePreviewPath
                filePath
                fileType
            }
        }
    }
    """,
    "variables": {"id": "662942"}
}
req = urllib.request.Request(url, data=json.dumps(query).encode("utf-8"), headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(json.dumps(data, indent=2))
except Exception as e:
    print("Error:", e)
