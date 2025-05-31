from __future__ import annotations

import typing as t
import uuid

import pydantic as pdt

from aiidalab_qe.common.components.wizard.state import WizardState
from aiidalab_qe.common.models.utils import ConfiguredBaseModel

WDM = t.TypeVar("WDM", bound=pdt.BaseModel)


class WizardModel(ConfiguredBaseModel, t.Generic[WDM]):
    uid: str = pdt.Field(default_factory=lambda: str(uuid.uuid4()))
    current_step: t.Optional[int] = None
    states: list[WizardState] = pdt.Field(default_factory=list)
    data: t.Optional[WDM] = None
