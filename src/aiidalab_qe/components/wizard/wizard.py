from __future__ import annotations

import solara
from solara.tasks import use_task
from solara.toestand import Ref

from aiidalab_qe.common.components.wizard import Wizard
from aiidalab_qe.common.services.aiida import AiiDAService

from .models import QeWizardModel
from .steps import QE_WIZARD_STEPS


@solara.component
def QeWizard(model: solara.Reactive[QeWizardModel]):
    label = Ref(model.fields.data.label)
    description = Ref(model.fields.data.description)
    input_structure = Ref(model.fields.data.input_structure)
    data = Ref(model.fields.data)
    process = Ref(model.fields.data.process)

    submitting = solara.use_reactive(False)

    async def submit_workflow():
        if not submitting.value:
            return
        inputs = {
            "label": label.value,
            "description": description.value,
            "input_structure": input_structure.value,
            **data.value.to_legacy_parameters(),
        }
        process_uuid = await AiiDAService.submit(inputs)
        process.set(process_uuid)

    use_task(
        submit_workflow,
        dependencies=[submitting.value],
    )

    with solara.Div(class_="qe-wizard"):
        solara.HTML("h2", label.value)
        Wizard(
            steps=QE_WIZARD_STEPS,
            model=model,
            submit_callback=lambda: submitting.set(True),
        )
