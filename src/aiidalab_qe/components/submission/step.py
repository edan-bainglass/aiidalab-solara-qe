from __future__ import annotations

import solara
import solara.toestand

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.components.wizard.models import QeWizardModel
from aiidalab_qe.config.paths import STYLES


@solara.component
def SubmissionStep(
    model: solara.Reactive[QeWizardModel],
    on_state_change: onStateChange,
):
    print("\nrendering submission-step component")

    process = solara.toestand.Ref(model.fields.data.process)

    def update_state():
        if not process.value:
            new_state = WizardState.INIT
        else:
            if not process.value.is_finished:
                new_state = WizardState.ACTIVE
            elif process.value.is_finished_ok:
                new_state = WizardState.SUCCESS
            else:
                new_state = WizardState.FAIL

        on_state_change(new_state)

    solara.use_effect(update_state, [process.value])

    with solara.Head():
        solara.Style(STYLES / "submission.css")

    with solara.Div(class_="submission-step"):
        solara.Text("placeholder for workflow submission")
