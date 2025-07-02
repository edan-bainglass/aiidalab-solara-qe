from __future__ import annotations

import solara

from aiidalab_qe.components import QeNavBar
from aiidalab_qe.config.paths import STYLES
from aiidalab_qe.pages import CalculationHistory, Home, ResourceSetup, Workbench

# from aiidalab_qe.pages.tester import Tester, TesterLayout

pages = {
    "home": {
        "link": "/",
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
    # "tester": {
    #     "link": "tester",
    #     "component": Tester,
    #     "layout": TesterLayout,
    # },
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
        layout=Layout if page == "home" else page_data.get("layout"),
    )
    for page, page_data in pages.items()
]
