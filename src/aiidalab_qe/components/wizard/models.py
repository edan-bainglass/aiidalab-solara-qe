from __future__ import annotations

import typing as t

import ase
from aiida.engine import ProcessState
from pydantic import model_validator

from aiidalab_qe.common.components.wizard import WizardDataModel
from aiidalab_qe.common.components.wizard.models import WizardModel
from aiidalab_qe.common.components.wizard.state import WizardState
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


class QeWizardModel(WizardModel):
    pk: t.Optional[int] = None

    @model_validator(mode="after")
    def _from_pk(self):
        if self.pk:
            process = AiiDAService.load_qe_app_workflow_node(self.pk)
            if not process.process_state:
                results_state = WizardState.INIT
            elif process.is_finished:
                if process.exit_status == 0:
                    results_state = WizardState.SUCCESS
                else:
                    results_state = WizardState.FAIL
            else:
                results_state = WizardState.ACTIVE
            self.states = [WizardState.SUCCESS] * 4 + [results_state]
            self.current_step = len(self.states) - 1
        else:
            self.states = [WizardState.READY, *[WizardState.INIT] * 4]
            self.current_step = None
        return self


class QeDataModel(WizardDataModel[QeAppModel]):
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
    def _from_pk(self):
        self.data = self.data or (from_process(self.pk) if self.pk else QeAppModel())
        return self
