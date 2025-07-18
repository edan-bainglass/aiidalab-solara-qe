from __future__ import annotations

import typing as t

import solara
from solara.toestand import Ref

from aiidalab_qe.config.paths import STYLES

from .models import WDM, WizardModel
from .state import BG_COLORS, STATE_ICONS, WizardState
from .types import WizardStepProps


@solara.component
def Wizard(
    steps: list[WizardStepProps],
    model: solara.Reactive[WizardModel],
    submit_callback: t.Callable[[], None] = None,
):
    print("rendering wizard component")

    current_step = Ref(model.fields.current_step)
    states = Ref(model.fields.states)

    render_context = solara.reacton.core.get_render_context()

    def update_state(index: int, new_state: WizardState):
        with render_context:
            if states.value[index] == new_state:
                return

            new_states: list = states.value[:]
            new_states[index] = new_state

            def reset_subsequent_steps():
                next_steps_count = len(new_states) - index - 1
                new_states[index + 1 :] = [WizardState.INIT] * next_steps_count

            def redirect_to_next_step():
                current_step.value += 1
                new_states[index + 1] = WizardState.CONFIGURED

            if current_step.value is not None and current_step.value < len(steps) - 1:
                if new_state is WizardState.CONFIGURED:
                    reset_subsequent_steps()
                if new_state is WizardState.SUCCESS:
                    redirect_to_next_step()

            states.set(new_states)

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
                v_model=current_step.value,
                on_v_model=current_step.set,
            ):
                for i, step in enumerate(steps):
                    state = states.value[i]
                    with solara.v.ExpansionPanel(class_="accordion-item"):
                        with solara.v.ExpansionPanelHeader(
                            class_="accordion-header",
                            style_=f"background-color: {BG_COLORS[state.name]}",
                        ):
                            WizardStepHeader(i, step, state)
                        with solara.v.ExpansionPanelContent(
                            class_="accordion-collapse"
                        ):
                            WizardStepBody(
                                i,
                                step,
                                state,
                                update_state,
                                Ref(model.fields.data),
                                i < len(steps) - 1,
                                submit_callback=submit_callback,
                            )


@solara.component
def WizardStepHeader(index: int, step: WizardStepProps, state: WizardState):
    with solara.Div(class_="accordion-header-content"):
        solara.v.Icon(
            class_="accordion-header-icon",
            left=True,
            children=[STATE_ICONS[state.name]],
        )
        solara.Text(
            f"Step {index + 1}: {step['title']}",
            classes=["accordion-header-text"],
        )


@solara.component
def WizardStepBody(
    index: int,
    step: WizardStepProps,
    state: WizardState,
    on_state_change: t.Callable[[int, WizardState], None],
    model: solara.Reactive[WDM],
    confirmable: bool = True,
    submit_callback: t.Callable[[], None] = None,
):
    def update_state(new_state: WizardState):
        if state in (WizardState.READY, WizardState.SUCCESS):
            on_state_change(index, new_state)

    def confirm_step():
        on_state_change(index, WizardState.SUCCESS)

    def submit_wizard():
        on_state_change(index, WizardState.SUCCESS)
        submit_callback()

    with solara.Div(class_="wizard-step-body"):
        with solara.Div(class_="wizard-step"):
            step["component"](model, update_state)

        if confirmable:
            with solara.Div(class_="wizard-step-controls"):
                if step.get("is_submission_step", False):
                    solara.Button(
                        label="Submit",
                        color="success",
                        icon_name="mdi-rocket",
                        disabled=state is not WizardState.CONFIGURED,
                        on_click=submit_wizard,
                    )
                else:
                    solara.Button(
                        label="Confirm",
                        color="success",
                        icon_name="check",
                        disabled=state is not WizardState.CONFIGURED,
                        on_click=confirm_step,
                    )
