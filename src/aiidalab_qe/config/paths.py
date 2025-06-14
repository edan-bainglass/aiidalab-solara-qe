from pathlib import Path

import aiidalab_qe

ROOT = Path(aiidalab_qe.__file__).parent
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
STYLES = ASSETS / "css"
IMAGES = ASSETS / "images"
COMPONENTS = ROOT / "components"
