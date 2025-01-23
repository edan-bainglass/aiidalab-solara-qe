from __future__ import annotations

import solara
from solara.alias import rv

from aiidalab_qe.common.components.wizard.models import WizardModel
from aiidalab_qe.common.components.wizard.state import BG_COLORS, STATE_ICONS, State

from .step import StepProps, WizardStep


@solara.component
def Wizard(steps: list[StepProps], model: WizardModel):
    selected_index = solara.use_reactive(model.current_step.value)
    initialized = solara.use_reactive(False)

    def handle_state(i: int, new_state: State):
        new_states: list = model.states.value[:]
        new_states[i] = new_state

        if (
            new_state is State.SUCCESS
            and selected_index is not None
            and selected_index < len(steps) - 1
        ):
            new_states[i + 1] = State.CONFIGURED
            selected_index.set(selected_index + 1)

        model.states.set(new_states)

    def initialize_wizard():
        if not initialized.value:
            model.states.set([State.READY, *[State.INIT] * (len(steps) - 1)])
        initialized.set(True)

    solara.use_effect(initialize_wizard, [])

    if not initialized.value:
        with rv.Container(class_="d-flex justify-content-center"):
            solara.SpinnerSolara()
    else:
        solara.SpinnerSolara()
        with rv.ExpansionPanels(
            class_="accordion gap-2",
            hover=True,
            accordion=True,
            v_model=selected_index,
            on_v_model=lambda i: selected_index.set(i),
        ):
            for i, step in enumerate(steps):
                with rv.ExpansionPanel(class_="accordion-item"):
                    with rv.ExpansionPanelHeader(
                        class_="accordion-header align-items-center justify-content-start",
                        style_=f"background-color: {BG_COLORS[model.states.value[i]]}",
                    ):
                        with rv.Container(class_="d-flex p-0"):
                            rv.Icon(
                                style_="margin-bottom: 1px; width: 30px;",
                                left=True,
                                children=[STATE_ICONS[model.states.value[i]]],
                            )
                            rv.Text(
                                class_="align-self-end",
                                children=[f"Step {i + 1}: {step['title']}"],
                            )
                    with rv.ExpansionPanelContent(class_="accordion-collapse"):
                        WizardStep(
                            state=model.states.value[i],
                            component=step["component"],
                            model=model,
                            on_state_change=lambda state, i=i: handle_state(i, state),
                            confirmable=i < len(steps) - 1,
                        )
