from __future__ import annotations

import solara
from aiida import load_profile
from solara.alias import rv

from aiidalab_qe.common.config.paths import STYLES
from aiidalab_qe.components import QeNavBar
from aiidalab_qe.pages import CalculationHistory, Home, ResourceSetup, Workbench

_ = load_profile()


@solara.component
def Layout(children=[]):
    QeNavBar()
    with rv.Container(class_="d-none"):
        with solara.Head():
            solara.Title("AiiDAlab QE app")
            solara.Style(STYLES / "main.css")
    solara.Div(children=children)


@solara.component
def Test():
    with solara.Sidebar():
        with rv.ListGroup():
            with rv.ListItem():
                solara.Text("1")
            with rv.ListItem():
                solara.Text("2")
            with rv.ListItem():
                solara.Text("3")
            with rv.ListItem():
                solara.Text("4")
    with rv.Container(class_="mt-5"):
        rv.Html(tag="h1", children=["Test"])


routes = [
    # solara.Route(path="/", component=Test, layout=solara.AppLayout),
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
