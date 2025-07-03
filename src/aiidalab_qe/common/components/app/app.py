from __future__ import annotations

import typing as t

import solara

from ..header import Header
from ..navbar import NavBar
from ..navbar.types import NavItemProps


@solara.component
def App(
    title: str,
    subtitle: str = "",
    logo: t.Optional[dict] = None,
    nav_items: t.Optional[list[NavItemProps]] = None,
    children: t.Optional[list[solara.Element]] = None,
):
    with solara.v.Container():
        Header(title, subtitle, logo)
        if nav_items:
            NavBar(nav_items)
        solara.v.Container(children=children or [])
