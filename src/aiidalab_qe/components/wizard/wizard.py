from __future__ import annotations

import solara
from solara.alias import rv

from aiidalab_qe.common.components import Wizard
from aiidalab_qe.components.wizard.models import WorkflowModel

from ..parameters import ParametersConfigurationStep
from ..resources import ResourcesSelectionStep
from ..results import ResultsStep
from ..structure import StructureSelectionStep
from ..submission import SubmissionStep


@solara.component
def QeWizard(model: solara.Reactive[WorkflowModel]):
    rv.Html(tag="h2", class_="text-center", children=[model.value.label])
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
            model=model,
        )
