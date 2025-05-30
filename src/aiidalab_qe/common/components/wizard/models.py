from __future__ import annotations

import typing as t

import pydantic as pdt

from aiidalab_qe.common.components.wizard.state import WizardState


class WizardModel(pdt.BaseModel):
    current_step: t.Optional[int] = None
    states: t.Optional[list[WizardState]] = None


WDM = t.TypeVar("WDM", bound=pdt.BaseModel)


class WizardDataModel(pdt.BaseModel, t.Generic[WDM]):
    data: t.Optional[WDM] = None
