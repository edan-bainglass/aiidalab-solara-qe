from __future__ import annotations

import solara

from .logo import Logo, LogoProps


@solara.component
def Header(title: str, subtitle: str = "", logo: LogoProps | None = None):
    if logo:
        Logo(**logo)
    with solara.v.Container(class_="text-center"):
        solara.v.Html(
            tag="h1",
            class_="display-5 fw-bold",
            children=[title],
        )
        if subtitle:
            solara.v.Html(
                tag="h2",
                class_="lead mx-auto py-2",
                children=[subtitle],
            )
