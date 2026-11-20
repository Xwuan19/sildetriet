import urllib.request

url = "https://commons.wikimedia.org/wiki/Special:FilePath/Brodskiy%20II%20Lenin.jpg"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp, open("preview_red/brodsky_lenin.jpg", "wb") as out:
        out.write(resp.read())
    print("Downloaded brodsky_lenin.jpg successfully!")
except Exception as e:
    print("Failed to download:", e)
