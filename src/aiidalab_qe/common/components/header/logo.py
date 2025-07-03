from __future__ import annotations

import typing as t
from pathlib import Path

import solara


@solara.component
def Logo(src: t.Union[Path, str], alt: str = "", width: str = "100px"):
    solara.Image(
        image=src,
        format="svg",
        width=width,
        classes=["d-block", "mx-auto"],
    )
