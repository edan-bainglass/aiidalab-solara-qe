from __future__ import annotations

import solara

from aiidalab_qe.components import QeNavBar
from aiidalab_qe.config.paths import STYLES
from aiidalab_qe.pages import CalculationHistory, Home, ResourceSetup, Workbench

# from aiidalab_qe.pages.tester import Tester, TesterLayout

pages = {
    "home": {
        "link": "aiidalab-qe",
        "component": Home,
    },
    "workbench": {
        "link": "aiidalab-qe/workbench",
        "component": Workbench,
    },
    "history": {
        "link": "aiidalab-qe/history",
        "component": CalculationHistory,
    },
    "resources": {
        "link": "aiidalab-qe/resources",
        "component": ResourceSetup,
    },
    # "tester": {
    #     "link": "aiidalab-qe/tester",
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
        path="aiidalab-qe",
        children=[
            solara.Route(
                path="/" if page == "home" else page,
                component=page_data["component"],
                layout=page_data.get("layout"),
            )
            for page, page_data in pages.items()
        ],
        layout=Layout,
    ),
]
