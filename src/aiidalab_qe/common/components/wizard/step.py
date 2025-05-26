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
    def update_state(new_state: WizardState):
        if new_state.value == state.value:
            return
        if state in (WizardState.READY, WizardState.SUCCESS):
            on_state_change(new_state)

    with solara.Div(class_="wizard-step"):
        print("\nrendering wizard step component")
        component(data_model, update_state)
        with solara.Div(class_="wizard-step-controls"):
            if confirmable:
                solara.Button(
                    label="Confirm",
                    color="success",
                    icon_name="check",
                    disabled=state is not WizardState.CONFIGURED,
                    on_click=lambda: on_state_change(WizardState.SUCCESS),
                )
