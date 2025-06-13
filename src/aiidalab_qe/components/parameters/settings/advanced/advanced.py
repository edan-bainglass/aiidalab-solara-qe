from __future__ import annotations

import solara
from aiida import orm
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import CalculationParametersModel

from .convergence import ConvergenceSettings
from .smearing import SmearingSettings

CATEGORIES = {
    "Convergence": ConvergenceSettings,
    "Smearing": SmearingSettings,
}


@solara.component
def AdvancedSettings(
    input_structure: solara.Reactive[orm.StructureData],
    parameters: solara.Reactive[CalculationParametersModel],
):
    spin_type = Ref(parameters.fields.basic.spin_type)
    active_panel = solara.use_reactive("Convergence")

    with solara.Row(classes=["mb-2"]):
        with solara.Column():
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

    CATEGORIES[active_panel.value](input_structure, parameters)
