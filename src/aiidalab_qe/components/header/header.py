from __future__ import annotations

import solara
from solara.alias import rv

from .logo import Logo, LogoProps


@solara.component
def Header(title: str, subtitle: str = "", logo: LogoProps | None = None):
    if logo:
        Logo(**logo)
    with rv.Container(class_="text-center"):
        rv.Html(
            tag="h1",
            class_="display-5 fw-bold",
            children=[title],
        )
        if subtitle:
            rv.Html(
                tag="h2",
                class_="lead mx-auto py-2 text-center",
                children=[subtitle],
            )
