from __future__ import annotations

import typing as t

from pydantic import BaseModel, model_validator

from aiidalab_qe.common.components.wizard.state import WizardState
from aiidalab_qe.common.services.aiida import AiiDAService


# TODO remove pk dependency to keep general
class WizardModel(BaseModel):
    pk: t.Optional[int] = None
    current_step: t.Optional[int] = None
    states: t.Optional[list[WizardState]] = None

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
        return self


WDM = t.TypeVar("WDM", bound=BaseModel)


class WizardDataModel(BaseModel, t.Generic[WDM]):
    data: t.Optional[WDM] = None
