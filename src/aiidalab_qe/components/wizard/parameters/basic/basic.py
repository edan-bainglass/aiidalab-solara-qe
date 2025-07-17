from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.common.components.selection import ToggleButtons
from aiidalab_qe.common.models.schema import QeAppModel


@solara.component
def BasicSettings(active: bool, model: solara.Reactive[QeAppModel]):
    process = Ref(model.fields.process)
    parameters = model.fields.calculation_parameters.basic
    electronic_type = Ref(parameters.electronic_type)
    spin_type = Ref(parameters.spin_type)
    spin_orbit = Ref(parameters.spin_orbit)
    protocol = Ref(parameters.protocol)

    disabled = solara.use_memo(
        lambda: process.value is not None,
        [process.value],
    )

    with solara.Div(
        class_=" ".join(
            [
                "control-group basic-settings",
                *([] if active else ["d-none"]),
            ],
        ),
    ):
        if not active:
            return

        print("rendering basic-settings component")

        ToggleButtons(
            label="Electronic type",
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
            value=electronic_type,
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
            value=spin_type,
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
            value=spin_orbit,
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
            value=protocol,
            disabled=disabled,
            class_="protocol-selector",
        )
