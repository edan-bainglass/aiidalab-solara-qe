from __future__ import annotations

import solara
from solara.alias import rv

from aiidalab_qe.common.components.wizard import Wizard, WizardModel

from ..parameters import ParametersConfigurationStep
from ..resources import ResourcesSelectionStep
from ..results import ResultsStep
from ..structure import StructureSelectionStep
from ..submission import SubmissionStep
from .models import WorkflowDataModel


@solara.component
def QeWizard(
    wizard_model: solara.Reactive[WizardModel],
    data_model: solara.Reactive[WorkflowDataModel],
):
    print("\nrendering qe-wizard component")
    rv.Html(tag="h2", class_="text-center", children=[data_model.value.label])
    with rv.Container():
        Wizard(
            steps=[
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
            ],
            wizard_model=wizard_model,
            data_model=data_model,
        )
