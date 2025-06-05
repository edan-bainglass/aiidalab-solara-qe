from __future__ import annotations

import solara
import solara.toestand

from aiidalab_qe.common.components.wizard import Wizard
from aiidalab_qe.common.services.aiida import AiiDAService

from ..parameters import ParametersConfigurationStep
from ..resources import ResourcesSelectionStep
from ..results import ResultsStep
from ..structure import StructureSelectionStep
from ..submission import SubmissionStep
from .models import QeWizardModel

QE_WIZARD_STEPS = (
    {
        "title": "Select structure",
        "component": StructureSelectionStep,
    },
    {
        "title": "Configure the workflow",
        "component": ParametersConfigurationStep,
    },
    {
        "title": "Choose computational resources",
        "component": ResourcesSelectionStep,
    },
    {
        "title": "Submit the workflow",
        "component": SubmissionStep,
        "is_submission_step": True,
    },
    {
        "title": "Status & results",
        "component": ResultsStep,
    },
)


@solara.component
def QeWizard(model: solara.Reactive[QeWizardModel]):
    label = solara.toestand.Ref(model.fields.data.label)

    def submit_workflow():
        inputs = model.value.data.to_legacy_parameters()
        AiiDAService.submit(inputs)

    with solara.Div(class_="qe-wizard"):
        solara.HTML("h2", label.value)
        Wizard(
            steps=QE_WIZARD_STEPS,
            model=model,
            submit_callback=submit_workflow,
        )
