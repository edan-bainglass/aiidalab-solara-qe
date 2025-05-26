from __future__ import annotations

from aiidalab_qe.config.paths import STYLES
import solara
import solara.toestand

from aiidalab_qe.common.components.wizard.state import WizardState
from aiidalab_qe.common.components.wizard.step import onStateChange
from aiidalab_qe.components.wizard.models import QeDataModel


@solara.component
def SubmissionStep(
    data_model: solara.Reactive[QeDataModel],
    on_state_change: onStateChange,
):
    print("\nrendering submission-step component")

    process = solara.toestand.Ref(data_model.fields.data.process)

    def update_state():
        if not process.value:
            on_state_change(WizardState.READY)
        elif data_model.value.data.process:
            on_state_change(WizardState.SUCCESS)
        else:
            on_state_change(WizardState.CONFIGURED)

    solara.use_effect(update_state, [process.value])

    with solara.Head():
        solara.Style(STYLES / "submission.css")

    with solara.Div(class_="submission-step"):
        solara.Text("placeholder for workflow submission")
