from __future__ import annotations

import typing as t

import solara

from .models import WizardDataModel
from .state import WizardState

onStateChange = t.Callable[[WizardState], None]
WizardStepType = t.Callable[
    [
        solara.Reactive[WizardDataModel],
        onStateChange,
    ],
    solara.Element,
]


class WizardStepProps(t.TypedDict):
    title: str
    component: WizardStepType


@solara.component
def WizardStep(
    state: WizardState,
    component: WizardStepType,
    data_model: solara.Reactive[WizardDataModel],
    on_state_change: onStateChange,
    confirmable: bool = True,
):
    print("rendering wizard step component")
    component(data_model, on_state_change)
    if confirmable:
        solara.Button(
            label="Confirm",
            color="success",
            icon_name="check",
            disabled=state is not WizardState.CONFIGURED,
            on_click=lambda: on_state_change(WizardState.SUCCESS),
        )
