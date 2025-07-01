import solara
from solara.toestand import Ref

from aiidalab_qe.common.hooks.weas import use_weas
from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.common.services.aiida import AiiDAService


@solara.component
def StructureResults(model: solara.Reactive[QeAppModel]):
    process = Ref(model.fields.process)

    process_node = solara.use_memo(
        lambda: AiiDAService.load_process(process.value),
        [process.value],
    )

    viewer = use_weas(process_node.inputs.structure)

    if not viewer.value:
        with solara.Div(class_="spinner"):
            solara.SpinnerSolara()
    else:
        solara.Div(
            class_="structure-viewer card",
            children=[viewer.value],
        )
