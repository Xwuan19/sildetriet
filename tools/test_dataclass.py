from dataclasses import dataclass, asdict
import json
from typing import List, Dict, Optional

@dataclass
class TokenTest:
    primary: str
    fonts: List[str]

t = TokenTest(primary="#8E1A1E", fonts=["Playfair", "Be Vietnam Pro"])
print(json.dumps(asdict(t)))
