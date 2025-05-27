from __future__ import annotations

import solara

from aiidalab_qe.common.components.wizard import Wizard

from ..parameters import ParametersConfigurationStep
from ..resources import ResourcesSelectionStep
from ..results import ResultsStep
from ..structure import StructureSelectionStep
from ..submission import SubmissionStep
from .models import QeDataModel, QeWizardModel

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
    },
    {
        "title": "Status & results",
        "component": ResultsStep,
    },
)


@solara.component
def QeWizard(
    wizard_model: solara.Reactive[QeWizardModel],
    data_model: solara.Reactive[QeDataModel],
):
    print("\nrendering qe-wizard component")
    with solara.Div(class_="qe-wizard"):
        solara.HTML("h2", data_model.value.label)

        Wizard(
            steps=QE_WIZARD_STEPS,
            wizard_model=wizard_model,
            data_model=data_model,
        )
