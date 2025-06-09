import solara
from aiida import orm

from aiidalab_qe.common.hooks.weas import use_weas


@solara.component
def StructureResults(process: orm.ProcessNode):
    viewer = use_weas(process.inputs.structure)

    if not viewer.value:
        with solara.Div(class_="spinner"):
            solara.SpinnerSolara()
    else:
        solara.Div(
            class_="structure-viewer card",
            children=[viewer.value],
        )
