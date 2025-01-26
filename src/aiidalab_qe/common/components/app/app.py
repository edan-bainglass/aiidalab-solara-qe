from __future__ import annotations

import solara

from ..header import Header, LogoProps
from ..navbar import NavBar, NavItemProps


@solara.component
def App(
    title: str,
    subtitle: str = "",
    logo: LogoProps | None = None,
    nav_items: list[NavItemProps] | None = None,
    children: list[solara.Element] | None = None,
):
    with solara.v.Container():
        Header(title, subtitle, logo)
        if nav_items:
            NavBar(nav_items)
        solara.v.Container(children=children or [])
