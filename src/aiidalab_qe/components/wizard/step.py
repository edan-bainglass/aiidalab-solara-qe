from __future__ import annotations

import typing as t

import solara

from aiidalab_qe.common.state import State

onStateChange = t.Callable[[State], None]
WizardStepType = t.Callable[[onStateChange], solara.Element]


class StepProps(t.TypedDict):
    title: str
    component: WizardStepType


@solara.component
def WizardStep(
    component: WizardStepType,
    on_state_change: onStateChange,
    confirmable: bool = True,
):
    state, set_state = solara.use_state(State.INIT)

    def _on_state_change(new_state: State):
        on_state_change(new_state)

    solara.use_effect(lambda: _on_state_change(state), [state])

    component(set_state)

    if confirmable:
        solara.Button(
            label="Confirm",
            color="success",
            icon_name="check",
            disabled=state is not State.CONFIGURED,
            on_click=lambda: on_state_change(State.SUCCESS),
        )
