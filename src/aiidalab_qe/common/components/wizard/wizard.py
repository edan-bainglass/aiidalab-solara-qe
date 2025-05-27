from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.config.paths import STYLES

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

        def reset_subsequent_steps():
            next_steps_count = len(new_states) - index - 1
            new_states[index + 1 :] = [WizardState.INIT] * next_steps_count

        def redirect_to_next_step():
            selected_index.value += 1
            new_states[index + 1] = WizardState.CONFIGURED

        if selected_index.value is not None and selected_index.value < len(steps) - 1:
            if new_state is WizardState.CONFIGURED:
                reset_subsequent_steps()
            if new_state is WizardState.SUCCESS:
                redirect_to_next_step()

        states.value = new_states

    with solara.Head():
        solara.Style(STYLES / "wizard.css")

    with solara.Div(class_="wizard"):
        if not states.value:
            with solara.Div(class_="spinner"):
                solara.SpinnerSolara()
        else:
            with solara.v.ExpansionPanels(
                class_="accordion",
                hover=True,
                accordion=True,
                v_model=selected_index.value,
                on_v_model=lambda i: selected_index.set(i),
            ):
                for i, step in enumerate(steps):
                    with solara.v.ExpansionPanel(class_="accordion-item"):
                        with solara.v.ExpansionPanelHeader(
                            class_="accordion-header",
                            style_=f"background-color: {BG_COLORS[states.value[i].name]}",
                        ):
                            with solara.Div(class_="accordion-header-content"):
                                solara.v.Icon(
                                    class_="accordion-header-icon",
                                    left=True,
                                    children=[STATE_ICONS[states.value[i].name]],
                                )
                                solara.Text(
                                    f"Step {i + 1}: {step['title']}",
                                    classes=["accordion-header-text"],
                                )
                        with solara.v.ExpansionPanelContent(
                            class_="accordion-collapse"
                        ):
                            on_state_change = solara.use_memo(
                                lambda: lambda state, i=i: update_states(i, state),
                                dependencies=[],
                            )
                            WizardStep(
                                state=states.value[i],
                                component=step["component"],
                                data_model=data_model,
                                on_state_change=on_state_change,
                                confirmable=i < len(steps) - 1,
                            )
