from __future__ import annotations

import typing as t

import solara

from aiidalab_qe.common.components.wizard.models import WizardModel
from aiidalab_qe.common.components.wizard.state import State

onStateChange = t.Callable[[State], None]
WizardStepType = t.Callable[[WizardModel, onStateChange], solara.Element]


class StepProps(t.TypedDict):
    title: str
    component: WizardStepType


@solara.component
def WizardStep(
    state: State,
    component: WizardStepType,
    model: WizardModel,
    on_state_change: onStateChange,
    confirmable: bool = True,
):
    component(model, on_state_change)
    if confirmable:
        solara.Button(
            label="Confirm",
            color="success",
            icon_name="check",
            disabled=state is not State.CONFIGURED,
            on_click=lambda: on_state_change(State.SUCCESS),
        )
