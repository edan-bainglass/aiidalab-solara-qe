from __future__ import annotations

import typing as t

from aiidalab_qe.common.models.schema import QeAppModel
import solara
from solara.alias import rv

from aiidalab_qe.common.components.wizard.state import BG_COLORS, STATE_ICONS, State

from .step import StepProps, WizardStep


@solara.component
def Wizard(steps: list[StepProps], model: QeAppModel):
    selected_index, set_selected_index = solara.use_state(t.cast(int, None))
    states, set_states = solara.use_state([State.INIT for _ in steps])

    def handle_state(i: int, new_state: State):
        new_states = states[:]
        new_states[i] = new_state

        if (
            new_state is State.SUCCESS
            and selected_index is not None
            and selected_index < len(steps) - 1
        ):
            new_states[i + 1] = State.CONFIGURED
            set_selected_index(selected_index + 1)

        set_states(new_states)

    with rv.ExpansionPanels(
        class_="accordion gap-2",
        hover=True,
        accordion=True,
        v_model=selected_index,
        on_v_model=lambda i: set_selected_index(i),
    ):
        for i, step in enumerate(steps):
            with rv.ExpansionPanel(class_="accordion-item"):
                with rv.ExpansionPanelHeader(
                    class_="accordion-header align-items-center justify-content-start",
                    style_=f"background-color: {BG_COLORS[states[i]]}",
                ):
                    with rv.Container(class_="d-flex p-0"):
                        rv.Icon(
                            style_="margin-bottom: 1px; width: 30px;",
                            left=True,
                            children=[STATE_ICONS[states[i]]],
                        )
                        rv.Text(
                            class_="align-self-end",
                            children=[f"Step {i + 1}: {step['title']}"],
                        )
                with rv.ExpansionPanelContent(class_="accordion-collapse"):
                    WizardStep(
                        state=states[i],
                        component=step["component"],
                        model=model,
                        on_state_change=lambda state, i=i: handle_state(i, state),
                        confirmable=i < len(steps) - 1,
                    )
