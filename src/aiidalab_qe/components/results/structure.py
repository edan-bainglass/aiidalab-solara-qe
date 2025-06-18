from aiidalab_qe.common.types import ProcessType
import solara

from aiidalab_qe.common.hooks.weas import use_weas


@solara.component
def StructureResults(process: ProcessType):
    viewer = use_weas(process.inputs.structure)

    if not viewer.value:
        with solara.Div(class_="spinner"):
            solara.SpinnerSolara()
    else:
        solara.Div(
            class_="structure-viewer card",
            children=[viewer.value],
        )
