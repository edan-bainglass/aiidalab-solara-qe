from pathlib import Path

import aiidalab_qe

ROOT = Path(aiidalab_qe.__file__).parent
ASSETS = ROOT / "assets"
STYLES = ASSETS / "styles/css"
IMAGES = ASSETS / "images"
COMPONENTS = ROOT / "components"
