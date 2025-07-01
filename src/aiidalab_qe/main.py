from __future__ import annotations

import solara

from aiidalab_qe.components import QeNavBar
from aiidalab_qe.config.paths import APP_URL_ROOT, STYLES
from aiidalab_qe.pages import CalculationHistory, Home, ResourceSetup, Workbench

# from aiidalab_qe.pages.tester import Tester, TesterLayout

pages = {
    "home": {
        "link": APP_URL_ROOT,
        "component": Home,
    },
    "workbench": {
        "link": f"{APP_URL_ROOT}/workbench",
        "component": Workbench,
    },
    "history": {
        "link": f"{APP_URL_ROOT}/history",
        "component": CalculationHistory,
    },
    "resources": {
        "link": f"{APP_URL_ROOT}/resources",
        "component": ResourceSetup,
    },
    # "tester": {
    #     "link": f"{APP_URL_ROOT}/tester",
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
        path=APP_URL_ROOT,
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
