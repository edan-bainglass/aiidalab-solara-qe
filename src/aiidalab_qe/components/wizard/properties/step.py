import solara
from solara.toestand import Ref

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.config.paths import STYLES

from .properties import PropertiesSelector
from .relaxation import RelaxationSelector


@solara.component
def PropertiesSelectionStep(
    model: solara.Reactive[QeAppModel],
    on_state_change: onStateChange,
):
    process = Ref(model.fields.process)
    properties = Ref(model.fields.properties)
    relax_type = Ref(model.fields.calculation_parameters.relax_type)

    disabled = solara.use_memo(
        lambda: process.value is not None,
        [process.value],
    )

    def update_state():
        if disabled:
            return

        new_state = WizardState.CONFIGURED
        on_state_change(new_state)

    solara.use_effect(
        update_state,
        [properties.value, relax_type.value],
    )

    with solara.Head():
        solara.Style(STYLES / "properties.css")

    with solara.Div(class_="properties-step"):
        print("rendering properties-selection-step component")

        RelaxationSelector(model)

        solara.HTML("hr")

        PropertiesSelector(model)
