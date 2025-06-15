from __future__ import annotations

import solara
from aiida import orm
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import CalculationParametersModel

from .convergence import ConvergenceSettings
from .hubbard import HubbardUSettings
from .smearing import SmearingSettings

CATEGORIES = {
    "Convergence": ConvergenceSettings,
    "Smearing": SmearingSettings,
    "Hubbard U": HubbardUSettings,
}


@solara.component
def AdvancedSettings(
    active: bool,
    input_structure: solara.Reactive[orm.StructureData],
    parameters: solara.Reactive[CalculationParametersModel],
):
    spin_type = Ref(parameters.fields.basic.spin_type)
    active_panel = solara.use_reactive("Convergence")

    with solara.Div(class_="advanced-settings"):
        with solara.Row(classes=["mb-2"]):
            with solara.Column():
                if active:
                    solara.Select(
                        label="",
                        values=[
                            *filter(
                                lambda category: category != "Magnetization"
                                or spin_type.value == "collinear",
                                CATEGORIES,
                            )
                        ],
                        value=active_panel,
                    )

        for panel_key, AdvancedSettingsPanel in CATEGORIES.items():
            AdvancedSettingsPanel(
                active=active and active_panel.value == panel_key,
                input_structure=input_structure,
                parameters=parameters,
            )
