from __future__ import annotations

import solara
from solara.alias import rv

from ..header import Header, LogoProps
from ..navbar import NavBar, NavItemProps
from ..wizard import StepProps, Wizard


@solara.component
def App(
    title: str,
    subtitle: str = "",
    logo: LogoProps | None = None,
    nav_items: list[NavItemProps] | None = None,
    children: list[solara.Element] | None = None,
):
    with rv.Container(class_="text-center"):
        Header(title, subtitle, logo)
        if nav_items:
            NavBar(nav_items)
        rv.Container(children=children or [])


@solara.component
def WizardApp(
    title: str,
    subtitle: str = "",
    logo: LogoProps | None = None,
    nav_items: list[NavItemProps] | None = None,
    steps: list[StepProps] | None = None,
):
    App(
        title,
        subtitle,
        logo,
        nav_items,
        children=[Wizard(steps)],
    )
