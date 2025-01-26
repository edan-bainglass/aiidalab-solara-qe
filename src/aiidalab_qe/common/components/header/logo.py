from __future__ import annotations

from pathlib import Path

import solara

LogoProps = dict[str, str]


@solara.component
def Logo(src: Path | str, alt: str = "", width: int = 100):
    solara.v.Img(
        class_="d-block mx-auto",
        src=src.as_posix() if isinstance(src, Path) else src,
        alt=alt,
        width=width,
    )
