from __future__ import annotations

import typing as t

from pydantic import BaseModel

from aiidalab_qe.common.components.wizard.state import State

DM = t.TypeVar("DM", bound=BaseModel)


class WizardModel(BaseModel, t.Generic[DM]):
    current_step: t.Optional[int] = None
    states: t.Optional[list[State]] = None
    data: t.Optional[DM] = None
