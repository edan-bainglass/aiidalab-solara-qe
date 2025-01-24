from __future__ import annotations

import typing as t

import ase
from aiida.engine import ProcessState
from pydantic import model_validator

from aiidalab_qe.common.components.wizard.models import WizardModel
from aiidalab_qe.common.components.wizard.state import State
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
    pk: t.Optional[int] = None

    @property
    def label(self) -> str:
        if self.pk:
            if process := AiiDAService.load_qe_app_workflow_node(self.pk):
                return f"{process.label or 'Workflow'}"
        return "New workflow"

    @property
    def status_icon(self) -> str:
        icon_name = "egg"
        if self.pk:
            if process := AiiDAService.load_qe_app_workflow_node(self.pk):
                if process.is_failed:
                    icon_name = "close-thick"
                icon_name = STATUS_ICONS[process.process_state]
        return f"mdi-{icon_name}"

    def get_ase_structure(self) -> ase.Atoms | None:
        if self.data.input_structure:
            return self.data.input_structure.get_ase()

    @model_validator(mode="after")
    def _populate_model_from_pk(self):
        if self.pk:
            self.data = from_process(self.pk)
            process = self.data.process
            if not process.process_state:
                results_state = State.INIT
            elif process.is_finished:
                if process.exit_status == 0:
                    results_state = State.SUCCESS
                else:
                    results_state = State.FAIL
            else:
                results_state = State.ACTIVE
            self.states = [State.SUCCESS] * 4 + [results_state]
            self.current_step = 0
        self.data = self.data or (from_process(self.pk) if self.pk else QeAppModel())
        return self
