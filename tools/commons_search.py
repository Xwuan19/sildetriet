# -*- coding: utf-8 -*-
"""Tìm ảnh trên Wikimedia Commons và in ra thông tin giấy phép/kích thước."""
import json
import sys
import urllib.parse
import urllib.request

UA = "SildeTrietAssetBot/1.0 (educational slide deck; contact: local)"


def search(query, limit=25):
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": "6",
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|size|extmetadata",
        "iiurlwidth": "1200",
        "format": "json",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
    pages = data.get("query", {}).get("pages", {})
    out = []
    for page in pages.values():
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata") or {}
        out.append({
            "title": page.get("title", ""),
            "width": info.get("width", 0),
            "height": info.get("height", 0),
            "license": (meta.get("LicenseShortName") or {}).get("value", ""),
            "url": info.get("url", ""),
            "descriptionurl": info.get("descriptionurl", ""),
        })
    out.sort(key=lambda x: x["width"] * x["height"], reverse=True)
    return out


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "Vladimir Lenin portrait"
    for item in search(query):
        print(f"{item['width']}x{item['height']} | {item['license'][:28]:28s} | {item['title']}")
        print(f"    {item['url']}")
