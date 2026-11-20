import os
from pathlib import Path

# Check how slideppt_media was created
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".py"):
            try:
                content = Path(root, f).read_text(encoding="utf-8")
                if "slideppt_media" in content:
                    print(f"Found in {f}")
            except Exception:
                pass
