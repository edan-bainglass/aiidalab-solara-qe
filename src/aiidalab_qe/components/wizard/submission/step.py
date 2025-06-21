from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.config.paths import STYLES


@solara.component
def SubmissionStep(
    model: solara.Reactive[QeAppModel],
    on_state_change: onStateChange,
):
    print("\nrendering submission-step component")

    process = Ref(model.fields.process)
    label = Ref(model.fields.label)
    description = Ref(model.fields.description)

    def update_state():
        if not process.value:
            new_state = WizardState.READY
        else:
            new_state = WizardState.SUCCESS

        on_state_change(new_state)

    solara.use_effect(
        update_state,
        [process.value],
    )

    with solara.Head():
        solara.Style(STYLES / "submission.css")

    with solara.Div(class_="submission-step"):
        with solara.Row():
            with solara.Column(classes=["col-6", "p-0"]):
                solara.InputText(
                    label="Label",
                    value=label,
                    style="margin-bottom: 0.5rem;",
                )
                solara.InputTextArea(
                    label="Description",
                    value=description,
                    auto_grow=True,
                    rows=3,
                )
