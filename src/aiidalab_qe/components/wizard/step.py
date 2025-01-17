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
    component(on_state_change)
    if confirmable:
        solara.Button(
            label="Confirm",
            color="success",
            icon_name="check",
            on_click=lambda: on_state_change(State.SUCCESS),
        )
