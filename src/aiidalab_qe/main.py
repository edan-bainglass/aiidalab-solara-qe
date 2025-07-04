from __future__ import annotations

import solara

from aiidalab_qe.components import QeNavBar
from aiidalab_qe.config.deployment import BASE_URL
from aiidalab_qe.config.paths import STYLES
from aiidalab_qe.pages import CalculationHistory, Home, ResourceSetup, Workbench

pages = {
    "home": {
        "link": BASE_URL,
        "component": Home,
    },
    "workbench": {
        "link": f"{BASE_URL}/workbench",
        "component": Workbench,
    },
    "history": {
        "link": f"{BASE_URL}/history",
        "component": CalculationHistory,
    },
    "resources": {
        "link": f"{BASE_URL}/resources",
        "component": ResourceSetup,
    },
}


@solara.component
def Layout(children=[]):
    with solara.Head():
        solara.Title("AiiDAlab QE app")
        solara.Style(STYLES / "main.css")
    QeNavBar(pages)
    solara.Div(children=children)


def validate_link(link: str) -> str:
    return link.lstrip("/")


routes = [
    solara.Route(
        path=validate_link(page_data["link"]),
        component=page_data["component"],
        layout=Layout,
    )
    for page, page_data in pages.items()
]
