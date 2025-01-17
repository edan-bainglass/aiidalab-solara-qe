from __future__ import annotations

import typing as t

import solara

from aiidalab_qe.common.state import State

onStateChange = t.Callable[[State], None]
QeAppWizardStep = t.Callable[[onStateChange], solara.Element]
StepProps = tuple[str, QeAppWizardStep]


@solara.component
def WizardStep(
    step: QeAppWizardStep,
    on_state_change: onStateChange,
    confirmable: bool = True,
):
    step(on_state_change)
    if confirmable:
        solara.Button(
            label="Confirm",
            color="success",
            icon_name="check",
            on_click=lambda: on_state_change(State.SUCCESS),
        )
