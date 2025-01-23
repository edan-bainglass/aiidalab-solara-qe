from __future__ import annotations

import typing as t
from contextlib import contextmanager
import solara

from aiidalab_qe.common.models.schema import QeAppModel

workbench_context = solara.create_context([])


class WizardState(t.TypedDict):
    step: int
    state: QeAppModel


@contextmanager
def WizardStateProvider(children: list[solara.Element] | None = None):
    states, set_states = solara.use_state(t.cast(dict[str, WizardState], {}))

    def update_state(wizard_uuid: str, state: WizardState):
        set_states({**states, wizard_uuid: state})
