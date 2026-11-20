# -*- coding: utf-8 -*-
"""Liệt kê file trong một category Commons kèm kích thước/giấy phép."""
import json
import sys
import urllib.parse
import urllib.request

UA = "SildeTrietAssetBot/1.0 (educational slide deck; contact: local)"


def api(params):
    params = dict(params, format="json")
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def category_files(cat, limit=100):
    data = api({
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{cat}",
        "cmtype": "file",
        "cmlimit": str(limit),
    })
    titles = [m["title"] for m in data.get("query", {}).get("categorymembers", [])]
    files = []
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        info = api({
            "action": "query",
            "titles": "|".join(chunk),
            "prop": "imageinfo",
            "iiprop": "url|size|extmetadata",
            "format": "json",
        })
        for page in info.get("query", {}).get("pages", {}).values():
            ii = (page.get("imageinfo") or [{}])[0]
            meta = ii.get("extmetadata") or {}
            files.append({
                "title": page.get("title", ""),
                "width": ii.get("width", 0),
                "height": ii.get("height", 0),
                "license": (meta.get("LicenseShortName") or {}).get("value", ""),
                "url": ii.get("url", ""),
            })
    files.sort(key=lambda x: x["width"] * x["height"], reverse=True)
    return files


if __name__ == "__main__":
    cat = " ".join(sys.argv[1:]) or "Vladimir Lenin in 1918"
    for f in category_files(cat):
        if f["width"] >= 500:
            print(f"{f['width']}x{f['height']} | {f['license'][:24]:24s} | {f['title']}")
            print(f"    {f['url']}")
