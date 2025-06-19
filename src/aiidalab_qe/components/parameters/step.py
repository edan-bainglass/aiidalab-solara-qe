from __future__ import annotations

import typing as t

import solara
import solara.toestand

from aiidalab_qe.common.components.wizard import BG_COLORS, WizardState, onStateChange
from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.components.wizard.models import QeWizardModel
from aiidalab_qe.config.paths import STYLES

from .properties import PropertiesSelector
from .relaxation import RelaxationSelector
from .settings import CalculationSettings


@solara.component
def ParametersConfigurationStep(
    model: solara.Reactive[QeWizardModel],
    on_state_change: onStateChange,
):
    print("\nrendering parameters-configuration-step component")

    process = solara.toestand.Ref(model.fields.data.process)
    data_model = solara.toestand.Ref(model.fields.data)
    parameters = solara.toestand.Ref(model.fields.data.calculation_parameters)

    def update_state():
        if not parameters.value:
            new_state = WizardState.READY
        elif process.value:
            new_state = WizardState.SUCCESS
        else:
            new_state = WizardState.CONFIGURED

        on_state_change(new_state)

    solara.use_effect(
        update_state,
        [parameters.value],
    )

    def ParametersConfigurationSubstep(
        label: str,
        content: t.Callable[[t.Any], solara.Element],
        model: solara.Reactive[QeAppModel],
    ):
        with solara.v.ExpansionPanel(class_="accordion-item"):
            with solara.v.ExpansionPanelHeader(
                class_="accordion-header",
                style_=f"background-color: {BG_COLORS['INIT']}",
            ):
                with solara.Div(class_="accordion-header-content"):
                    solara.Text(label, classes=["accordion-header-text"])
            with solara.v.ExpansionPanelContent(class_="accordion-collapse"):
                content(model)

    with solara.Head():
        solara.Style(STYLES / "parameters.css")

    with solara.Div(class_="parameters-configuration-step"):
        RelaxationSelector(data_model)
        with solara.v.ExpansionPanels(class_="accordion"):
            ParametersConfigurationSubstep(
                label="Step 2.1: Select which properties to compute",
                content=PropertiesSelector,
                model=data_model,
            )
            ParametersConfigurationSubstep(
                label="Step 2.2: Customize calculation parameters",
                content=CalculationSettings,
                model=data_model,
            )
