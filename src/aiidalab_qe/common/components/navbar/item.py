from __future__ import annotations

import solara


@solara.component
def NavItem(label: str = "", icon: str = "", **kwargs):
    solara.v.Btn(
        class_="btn btn-hover m-1 justify-content-start",
        color="secondary",
        children=[
            solara.v.Icon(
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
