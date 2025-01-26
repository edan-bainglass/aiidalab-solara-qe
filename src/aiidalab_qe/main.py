from __future__ import annotations

import solara
from solara.alias import rv

from aiidalab_qe.components import QeNavBar
from aiidalab_qe.config.paths import STYLES
from aiidalab_qe.pages import CalculationHistory, Home, ResourceSetup, Workbench


@solara.component
def Layout(children=[]):
    QeNavBar()
    with rv.Container(class_="d-none"):
        with solara.Head():
            solara.Title("AiiDAlab QE app")
            solara.Style(STYLES / "main.css")
    solara.Div(children=children)


routes = [
    solara.Route(
        path="aiidalab-qe",
        children=[
            solara.Route(path="/", component=Home),
            solara.Route(path="workbench", component=Workbench),
            solara.Route(path="history", component=CalculationHistory),
            solara.Route(path="resources", component=ResourceSetup),
        ],
        layout=Layout,
    ),
]
