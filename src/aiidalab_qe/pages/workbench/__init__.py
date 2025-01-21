import solara
from solara.alias import rv

from .workbench import Workbench

__all__ = [
    "Workbench",
]


@solara.component
def Layout(children=[]):
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
    solara.Div(children=children)
