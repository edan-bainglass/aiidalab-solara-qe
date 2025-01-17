from __future__ import annotations

import solara

NavItemProps = dict[str, str]


@solara.component
def NavItem(label: str = "", icon: str = "", **kwargs):
    solara.Button(
        class_="btn btn-primary btn-lg m-1 justify-content-start",
        icon_name=f"mdi-{icon}",
        outlined=True,
        label=label,
        **kwargs,
    )


@solara.component
def LinkNavItem(label: str = "", icon: str = "", href: str = "", **kwargs):
    NavItem(label, icon, link=True, href=href, target="_blank", **kwargs)
