from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.common.components.wizard import onStateChange
from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.common.services.aiida import AiiDAService
from aiidalab_qe.config.paths import STYLES


@solara.component
def SubmissionStep(
    model: solara.Reactive[QeAppModel],
    on_state_change: onStateChange,
):
    print("rendering submission-step component")

    label = Ref(model.fields.label)
    description = Ref(model.fields.description)
    process = Ref(model.fields.process)

    process_node = AiiDAService.load_process(process.value)

    def update_label():
        if not process_node:
            return
        process_node.label = label.value

    def update_description():
        if not process_node:
            return
        process_node.description = description.value

    solara.use_effect(
        update_label,
        [process.value, label.value],
    )

    solara.use_effect(
        update_description,
        [process.value, description.value],
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
