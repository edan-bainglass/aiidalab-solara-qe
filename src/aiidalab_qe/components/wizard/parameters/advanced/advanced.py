from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import QeAppModel

from .convergence import ConvergenceSettings
from .hubbard import HubbardUSettings
from .magnetization import MagnetizationSettings
from .pseudos import PseudopotentialsSettings
from .smearing import SmearingSettings

CATEGORIES = {
    "Convergence": ConvergenceSettings,
    "Smearing": SmearingSettings,
    "Hubbard U": HubbardUSettings,
    "Pseudopotentials": PseudopotentialsSettings,
    "Magnetization": MagnetizationSettings,
}


@solara.component
def AdvancedSettings(active: bool, model: solara.Reactive[QeAppModel]):
    spin_type = Ref(model.fields.calculation_parameters.basic.spin_type)
    active_panel = solara.use_reactive("Convergence")

    def redirect_to_valid_panel():
        if spin_type.value == "none" and active_panel.value == "Magnetization":
            active_panel.set("Convergence")

    solara.use_effect(
        redirect_to_valid_panel,
        [spin_type.value],
    )

    with solara.Div(
        class_=" ".join(
            [
                "advanced-settings",
                *(["d-none"] if not active else []),
            ],
        ),
    ):
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
            classes=["parameters-category-selector"],
        )

        for panel_key, AdvancedSettingsPanel in CATEGORIES.items():
            AdvancedSettingsPanel(
                active=active and active_panel.value == panel_key,
                model=model,
            )
