import json

with open("archive/session/slide-morph-tri-t-h-c-m-c-l-nin.json", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def gradient_shape")
if idx != -1:
    print(text[idx:idx+1500])
