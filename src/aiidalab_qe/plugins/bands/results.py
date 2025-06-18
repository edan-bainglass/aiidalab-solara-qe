import solara
import solara.toestand

from aiidalab_qe.common.types import ProcessType


@solara.component
def BandStructureResults(process: ProcessType):
    with solara.Div(class_="results-panel"):
        solara.Text("Band structure results will be displayed here.")
