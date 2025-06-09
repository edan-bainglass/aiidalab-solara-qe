import solara
import solara.toestand
from aiida import orm


@solara.component
def BandStructureResults(process: orm.ProcessNode):
    with solara.Div(class_="results-panel"):
        solara.Text("Band structure results will be displayed here.")
