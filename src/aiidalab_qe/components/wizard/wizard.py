from __future__ import annotations

import typing as t

import solara
from reacton.core import UserContext
from solara.alias import rv

from aiidalab_qe.common.context import ContextProvider, ContextType
from aiidalab_qe.common.state import BG_COLORS, STATE_ICONS, State

from .step import StepProps, WizardStep


@solara.component
def Wizard(
    steps: list[StepProps],
    context: UserContext[ContextType] | None = None,
    defaults: ContextType | None = None,
):
    selected_index, set_selected_index = solara.use_state(t.cast(int, None))
    states, set_states = solara.use_state([State.INIT for _ in steps])

    def on_selection(index: int):
        set_selected_index(index)

    def on_state_change(i: int, new_state: State):
        set_states([*states[:i], new_state, *states[i + 1 :]])
        if (
            new_state is State.SUCCESS
            and selected_index
            and selected_index < len(steps) - 1
        ):
            set_selected_index(selected_index + 1)

    with ContextProvider(context, defaults):  # mypy: ignore
        with rv.ExpansionPanels(
            class_="accordion gap-1",
            hover=True,
            accordion=True,
            v_model=selected_index,
            on_v_model=on_selection,
        ):
            for i, step in enumerate(steps):
                with rv.ExpansionPanel(
                    class_="accordion-item",
                ):
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
                            component=step["component"],
                            on_state_change=lambda state, i=i: on_state_change(
                                i, state
                            ),
                            confirmable=i < len(steps) - 1,
                        )
