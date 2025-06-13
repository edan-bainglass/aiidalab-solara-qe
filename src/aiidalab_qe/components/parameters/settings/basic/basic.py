from __future__ import annotations

import solara
from aiida import orm
from solara.toestand import Ref

from aiidalab_qe.common.components.selection import ToggleButtons
from aiidalab_qe.common.models.schema import CalculationParametersModel


@solara.component
def BasicSettings(
    input_structure: solara.Reactive[orm.StructureData],
    parameters: solara.Reactive[CalculationParametersModel],
):
    basic_settings = parameters.fields.basic

    with solara.Div(class_="basic-settings"):
        ToggleButtons(
            reactive=Ref(basic_settings.electronic_type),
            label="Electronic Type",
            options={
                "metal": {
                    "label": "Metal",
                    "description": "Metallic system",
                },
                "insulator": {
                    "label": "Insulator",
                    "description": "Insulating system",
                },
            },
        )
        ToggleButtons(
            reactive=Ref(basic_settings.spin_type),
            label="Magnetism",
            options={
                "none": {
                    "label": "Off",
                    "description": "Magnetic system",
                },
                "collinear": {
                    "label": "On",
                    "description": "Non-magnetic system",
                },
            },
        )
        ToggleButtons(
            reactive=Ref(basic_settings.spin_orbit),
            label="Spin-orbit coupling",
            options={
                "wo_soc": {
                    "label": "Off",
                    "description": "Ignore spin-orbit coupling",
                },
                "soc": {
                    "label": "On",
                    "description": "Include spin-orbit coupling",
                },
            },
        )
        ToggleButtons(
            reactive=Ref(basic_settings.protocol),
            label="Protocol",
            options={
                "fast": {
                    "label": "Fast",
                    "description": "Reduced accuracy for quick results",
                },
                "balanced": {
                    "label": "Balanced",
                    "description": "Balanced accuracy and performance",
                },
                "stringent": {
                    "label": "Stringent",
                    "description": "High accuracy for demanding calculations",
                },
            },
            class_="protocol-selector",
        )
