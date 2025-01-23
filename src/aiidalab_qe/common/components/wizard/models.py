from __future__ import annotations

import typing as t

from solara import Reactive, reactive

from aiidalab_qe.common.models.reactive import ReactiveDataclass

DM = t.TypeVar("DM", bound=ReactiveDataclass)


class WizardModel(ReactiveDataclass, t.Generic[DM]):
    current_step: Reactive[int | None] = reactive(None)
    states: Reactive[list[int] | None] = reactive(None)
    data: DM | None = None
