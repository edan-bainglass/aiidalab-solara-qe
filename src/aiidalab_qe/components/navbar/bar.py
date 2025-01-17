from __future__ import annotations

import solara
from solara.alias import rv

from .item import LinkNavItem, NavItem, NavItemProps


@solara.component
def NavBar(items: list[NavItemProps]):
    with rv.Container(class_="d-grid d-md-block mb-3 p-0 justify-content-center"):
        for item in items:
            LinkNavItem(**item) if "href" in item else NavItem(**item)
