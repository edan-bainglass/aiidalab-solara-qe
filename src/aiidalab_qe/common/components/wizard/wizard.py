from __future__ import annotations

import solara
from solara.alias import rv
from solara.toestand import Ref

from .models import WizardDataModel, WizardModel
from .state import BG_COLORS, STATE_ICONS, WizardState
from .step import WizardStep, WizardStepProps


@solara.component
def Wizard(
    steps: list[WizardStepProps],
    wizard_model: solara.Reactive[WizardModel],
    data_model: solara.Reactive[WizardDataModel],
):
    print("\nrendering wizard component")
    selected_index = Ref(wizard_model.fields.current_step)
    states = Ref(wizard_model.fields.states)

    def update_states(index: int, new_state: WizardState):
        new_states: list = states.value[:]
        new_states[index] = new_state

        if (
            new_state is WizardState.SUCCESS
            and selected_index.value is not None
            and selected_index.value < len(steps) - 1
        ):
            new_states[index + 1] = WizardState.CONFIGURED
            selected_index.value += 1

        states.value = new_states

    def initialize_wizard():
        if not states.value:
            states.value = [WizardState.READY, *[WizardState.INIT] * (len(steps) - 1)]

    solara.use_effect(initialize_wizard, [])

    if not states.value:
        with rv.Container(class_="d-flex justify-content-center"):
            solara.SpinnerSolara()
    else:
        with rv.ExpansionPanels(
            class_="accordion gap-2",
            hover=True,
            accordion=True,
            v_model=selected_index.value,
            on_v_model=lambda i: selected_index.set(i),
        ):
            for i, step in enumerate(steps):
                with rv.ExpansionPanel(class_="accordion-item"):
                    with rv.ExpansionPanelHeader(
                        class_="accordion-header align-items-center justify-content-start",
                        style_=f"background-color: {BG_COLORS[states.value[i].name]}",
                    ):
                        with rv.Container(class_="d-flex p-0"):
                            rv.Icon(
                                style_="margin-bottom: 1px; width: 30px;",
                                left=True,
                                children=[STATE_ICONS[states.value[i].name]],
                            )
                            rv.Text(
                                class_="align-self-end",
                                children=[f"Step {i + 1}: {step['title']}"],
                            )
                    with rv.ExpansionPanelContent(class_="accordion-collapse"):
                        WizardStep(
                            state=states.value[i],
                            component=step["component"],
                            data_model=data_model,
                            on_state_change=lambda state, i=i: update_states(i, state),
                            confirmable=i < len(steps) - 1,
                        )
