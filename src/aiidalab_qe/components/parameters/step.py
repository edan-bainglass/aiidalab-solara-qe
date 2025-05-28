from __future__ import annotations

import solara
import solara.toestand

from aiidalab_qe.common.components.wizard.state import BG_COLORS, WizardState
from aiidalab_qe.common.components.wizard.step import onStateChange
from aiidalab_qe.components.wizard.models import QeDataModel
from aiidalab_qe.config.paths import STYLES

from .properties import PropertiesSelector
from .relaxation import RelaxationSelector
from .settings import CalculationSettings

SUB_STEPS = {
    "2.1": {
        "label": "Select which properties to compute",
        "component": PropertiesSelector,
    },
    "2.2": {
        "label": "Customize calculation parameters",
        "component": CalculationSettings,
    },
}


@solara.component
def ParametersConfigurationStep(
    data_model: solara.Reactive[QeDataModel],
    on_state_change: onStateChange,
):
    print("\nrendering parameters-configuration-step component")

    calculation_parameters = solara.toestand.Ref(
        data_model.fields.data.calculation_parameters
    )
    process = solara.toestand.Ref(data_model.fields.data.process)

    def update_state():
        if not calculation_parameters.value:
            on_state_change(WizardState.READY)
        elif process.value:
            on_state_change(WizardState.SUCCESS)
        else:
            on_state_change(WizardState.CONFIGURED)

    solara.use_effect(update_state, [calculation_parameters.value])

    with solara.Head():
        solara.Style(STYLES / "parameters.css")

    with solara.Div(class_="parameters-configuration-step"):
        RelaxationSelector(data_model)
        with solara.v.ExpansionPanels(class_="accordion"):
            for step, step_data in SUB_STEPS.items():
                with solara.v.ExpansionPanel(class_="accordion-item"):
                    with solara.v.ExpansionPanelHeader(
                        class_="accordion-header",
                        style_=f"background-color: {BG_COLORS['INIT']}",
                    ):
                        with solara.Div(class_="accordion-header-content"):
                            solara.Text(
                                f"Step {step}: {step_data['label']}",
                                classes=["accordion-header-text"],
                            )
                    with solara.v.ExpansionPanelContent(class_="accordion-collapse"):
                        step_data["component"](data_model)
