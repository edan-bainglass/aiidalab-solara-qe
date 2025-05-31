from __future__ import annotations

import solara
import solara.toestand

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.components.wizard.models import QeWizardModel
from aiidalab_qe.config.paths import STYLES


@solara.component
def ResourcesSelectionStep(
    model: solara.Reactive[QeWizardModel],
    on_state_change: onStateChange,
):
    print("\nrendering computational-resources-step component")

    computational_resources = solara.toestand.Ref(
        model.fields.data.computational_resources
    )
    process = solara.toestand.Ref(model.fields.data.process)

    def update_state():
        if not computational_resources.value:
            new_state = WizardState.READY
        elif process.value:
            new_state = WizardState.SUCCESS
        else:
            new_state = WizardState.CONFIGURED

        on_state_change(new_state)

    solara.use_effect(update_state, [computational_resources.value])

    with solara.Head():
        solara.Style(STYLES / "resources.css")

    with solara.Div(class_="resources-selection-step"):
        solara.Text("placeholder for computational resources selection")
