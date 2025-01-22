from __future__ import annotations

import solara
from solara.alias import rv

from aiidalab_qe.common.components import Wizard
from aiidalab_qe.common.models.schema import QeAppModel, from_process

from ..parameters import ParametersConfigurationStep
from ..resources import ResourcesSelectionStep
from ..results import ResultsStep
from ..structure import StructureSelectionStep
from ..submission import SubmissionStep


@solara.component
def QeWizard(pk: int | None = None):
    model = (
        from_process(pk)
        if pk
        else QeAppModel(
            input_structure=None,
            calculation_parameters={},
            computational_resources={},
            process=None,
        )
    )

    label = f"Workflow {f'[pk={pk}]' if pk else ''}"
    rv.Html(tag="h1", children=[label])
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
