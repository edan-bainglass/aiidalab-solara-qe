from __future__ import annotations

import solara

from aiidalab_qe.components import QeNavBar
from aiidalab_qe.config.paths import STYLES
from aiidalab_qe.pages import CalculationHistory, Home, ResourceSetup, Workbench

pages = {
    "home": {
        "link": "",
        "component": Home,
    },
    "workbench": {
        "link": "workbench",
        "component": Workbench,
    },
    "history": {
        "link": "history",
        "component": CalculationHistory,
    },
    "resources": {
        "link": "resources",
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


routes = [
    solara.Route(
        path=page_data["link"],
        component=page_data["component"],
        layout=Layout,
    )
    for page_data in pages.values()
]
