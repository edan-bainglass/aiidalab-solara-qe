from __future__ import annotations

import solara

from aiidalab_qe.config.paths import STYLES

from .item import LinkNavItem, NavItem
from .types import NavItemProps


@solara.component
def NavBar(items: list[NavItemProps]):
    with solara.Head():
        solara.Style(STYLES / "navbar.css")

    with solara.v.Container(
        class_="d-grid d-sm-block mb-3 p-0 justify-content-center text-center"
    ):
        for item in items:
            LinkNavItem(**item) if "href" in item else NavItem(**item)
