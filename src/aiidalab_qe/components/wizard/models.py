from __future__ import annotations


import ase
from aiida.engine import ProcessState
from pydantic import model_validator
from solara import Reactive, reactive

from aiidalab_qe.common.components.wizard.models import WizardModel
from aiidalab_qe.common.models.schema import QeAppModel, from_process
from aiidalab_qe.common.services.aiida import AiiDAService

STATUS_ICONS = {
    ProcessState.CREATED: "rocket-launch",
    ProcessState.WAITING: "time-sand-full",
    ProcessState.RUNNING: "time-sand-full",
    ProcessState.FINISHED: "check-bold",
    ProcessState.EXCEPTED: "alert-rhombus",
    ProcessState.KILLED: "skull",
}


class WorkflowModel(WizardModel[QeAppModel]):
    pk: Reactive[int | None] = reactive(None)

    @property
    def label(self) -> str:
        if self.pk.value:
            if process := AiiDAService.load_qe_app_workflow_node(self.pk.value):
                return f"{process.label or 'Workflow'}"
        return "New workflow"

    @property
    def status_icon(self) -> str:
        icon_name = "egg"
        if self.pk.value:
            if process := AiiDAService.load_qe_app_workflow_node(self.pk.value):
                if process.is_failed:
                    icon_name = "close-thick"
                icon_name = STATUS_ICONS[process.process_state]
        return f"mdi-{icon_name}"

    def get_ase_structure(self) -> ase.Atoms | None:
        if self.data.input_structure.value:
            return self.data.input_structure.value.get_ase()

    @model_validator(mode="after")
    def _populate_model_from_pk(self):
        print("Populating model from pk")
        self.data = self.data or (
            from_process(self.pk.value) if self.pk.value else QeAppModel()
        )
        return self
