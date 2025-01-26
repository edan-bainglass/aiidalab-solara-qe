from __future__ import annotations

import typing as t

from pydantic import BaseModel

from aiidalab_qe.common.components.wizard.state import WizardState


class WizardModel(BaseModel):
    current_step: t.Optional[int] = None
    states: t.Optional[list[WizardState]] = None


WDM = t.TypeVar("WDM", bound=BaseModel)


class WizardDataModel(BaseModel, t.Generic[WDM]):
    data: t.Optional[WDM] = None
