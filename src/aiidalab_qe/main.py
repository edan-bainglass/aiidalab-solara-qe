from __future__ import annotations

import solara
from solara.alias import rv

from aiidalab_qe.common.config.paths import STYLES
from aiidalab_qe.components import QeNavBar
from aiidalab_qe.pages import CalculationHistory, Home, ResourceSetup, Workbench
# from aiidalab_qe.common.context import workbench_context


@solara.component
def Layout(children=[]):
    QeNavBar()
    with rv.Container(class_="d-none"):
        with solara.Head():
            solara.Title("AiiDAlab QE app")
            solara.Style(STYLES / "main.css")
    solara.Div(children=children)


# @solara.component
# def WorkbenchWrapper():
#     workbench_context.provide([])
#     Workbench()


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
