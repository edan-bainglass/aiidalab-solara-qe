from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.common.components.selection import ToggleButtons
from aiidalab_qe.common.models.schema import QeAppModel


@solara.component
def BasicSettings(active: bool, model: solara.Reactive[QeAppModel]):
    process = Ref(model.fields.process)
    basic_settings = model.fields.calculation_parameters.basic

    disabled = solara.use_memo(
        lambda: process.value is not None,
        [process.value],
    )

    with solara.Div(
        class_=" ".join(
            [
                "control-group basic-settings",
                *(["d-none"] if not active else []),
            ],
        ),
    ):
        if not active:
            return

        print("\nrendering basic-settings component")

        ToggleButtons(
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
            value=Ref(basic_settings.electronic_type),
            disabled=disabled,
        )
        ToggleButtons(
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
            value=Ref(basic_settings.spin_type),
            disabled=disabled,
        )
        ToggleButtons(
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
            value=Ref(basic_settings.spin_orbit),
            disabled=disabled,
        )
        ToggleButtons(
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
            value=Ref(basic_settings.protocol),
            disabled=disabled,
            class_="protocol-selector",
        )
