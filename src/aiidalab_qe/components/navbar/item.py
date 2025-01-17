from __future__ import annotations

import solara
from solara.alias import rv

NavItemProps = dict[str, str]


@solara.component
def NavItem(label: str = "", icon: str = "", **kwargs):
    rv.Btn(
        class_="btn btn-hover m-1 justify-content-start",
        color="secondary",
        children=[
            rv.Icon(
                style_="margin-bottom: 1px;",
                left=bool(label),
                children=[f"mdi-{icon}"],
            ),
            label,
        ],
        **kwargs,
    )


@solara.component
def LinkNavItem(label: str = "", icon: str = "", href: str = "", **kwargs):
    NavItem(label, icon, link=True, href=href, target="_blank", **kwargs)
