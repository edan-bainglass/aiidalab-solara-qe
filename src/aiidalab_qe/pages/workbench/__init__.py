import solara
from solara.alias import rv

from .workbench import Workbench

__all__ = [
    "Workbench",
]


@solara.component
def Layout(children: list[solara.Element]):
    with solara.Sidebar():
        with rv.ListItem():
            solara.Text("<pk=93> Calculation 1")
    solara.Div(children=children)
