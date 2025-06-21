from __future__ import annotations

import solara
import solara.toestand

from aiidalab_qe.common.components.wizard import Wizard
from aiidalab_qe.common.services.aiida import AiiDAService

from .models import QeWizardModel
from .steps import QE_WIZARD_STEPS


@solara.component
def QeWizard(model: solara.Reactive[QeWizardModel]):
    label = solara.toestand.Ref(model.fields.data.label)

    def submit_workflow():
        inputs = {
            "label": model.value.data.label,
            "description": model.value.data.description,
            **model.value.data.to_legacy_parameters(),
        }
        AiiDAService.submit(inputs)

    with solara.Div(class_="qe-wizard"):
        solara.HTML("h2", label.value)
        Wizard(
            steps=QE_WIZARD_STEPS,
            model=model,
            submit_callback=submit_workflow,
        )
