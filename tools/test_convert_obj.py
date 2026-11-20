# -*- coding: utf-8 -*-
import sys
from pathlib import Path

cli_dir = Path("tools/sketchfab-cli").resolve()
sys.path.insert(0, str(cli_dir))

from osgjs_convert import convert_osgjs

work_dir = Path("assets/models3d/lenin_seattle").resolve()
res = convert_osgjs(work_dir, "Lenin_Seattle", prefer="obj")
print("Converted to:", res)
