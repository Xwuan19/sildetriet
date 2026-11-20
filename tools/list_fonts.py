from pathlib import Path

for p in sorted(Path("fonts").glob("*")):
    print(p.name)
