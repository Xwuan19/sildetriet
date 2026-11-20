from pathlib import Path

for p in sorted(Path("assets").glob("*")):
    print(f"assets/{p.name}: {p.stat().st_size} bytes")
