import urllib.request

url = "https://rusmuseumvrm.ru/data/collections/painting/19_20/brodskiy_i.i._lenin_na_tribune._1927._zhs-729/16451_mainfoto_03.jpg"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp, open("preview_red/lenin_tribune_original.jpg", "wb") as out:
        out.write(resp.read())
    print("Downloaded lenin_tribune_original.jpg successfully!")
except Exception as e:
    print("Failed 03, trying 02:", e)
    url = "https://rusmuseumvrm.ru/data/collections/painting/19_20/brodskiy_i.i._lenin_na_tribune._1927._zhs-729/16451_mainfoto_02.jpg"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp, open("preview_red/lenin_tribune_original.jpg", "wb") as out:
        out.write(resp.read())
    print("Downloaded lenin_tribune_original.jpg from 02!")
