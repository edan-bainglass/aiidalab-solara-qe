from __future__ import annotations

import solara
import solara.toestand

from aiidalab_qe.common.components.wizard.state import WizardState
from aiidalab_qe.common.components.wizard.step import onStateChange
from aiidalab_qe.components.wizard.models import QeDataModel
from aiidalab_qe.config.paths import STYLES


@solara.component
def ResourcesSelectionStep(
    data_model: solara.Reactive[QeDataModel],
    on_state_change: onStateChange,
):
    print("\nrendering computational-resources-step component")

    computational_resources = solara.toestand.Ref(
        data_model.fields.data.computational_resources
    )

    def update_state():
        if not computational_resources.value:
            on_state_change(WizardState.READY)
        elif data_model.value.data.process:
            on_state_change(WizardState.SUCCESS)
        else:
            on_state_change(WizardState.CONFIGURED)

    solara.use_effect(update_state, [computational_resources.value])

    with solara.Head():
        solara.Style(STYLES / "resources.css")

    with solara.Div(class_="resources-selection-step"):
        solara.Text("placeholder for computational resources selection")
