from __future__ import annotations

import typing as t

import solara
from solara.toestand import Ref

from aiidalab_qe.components.wizard.models import QeDataModel

CONTROLS = {
    "electronic_type": {
        "label": "Electronic type",
        "options": {
            "metal": {
                "label": "Metal",
                "description": "Metallic system",
            },
            "insulator": {
                "label": "Insulator",
                "description": "Insulating system",
            },
        },
    },
    "spin_type": {
        "label": "Magnetism",
        "options": {
            "none": {
                "label": "Off",
                "description": "Magnetic system",
            },
            "collinear": {
                "label": "On",
                "description": "Non-magnetic system",
            },
        },
    },
    "spin_orbit": {
        "label": "Spin-orbit coupling",
        "options": {
            "wo_soc": {
                "label": "Off",
                "description": "Ignore spin-orbit coupling",
            },
            "soc": {
                "label": "On",
                "description": "Include spin-orbit coupling",
            },
        },
    },
    "protocol": {
        "label": "Protocol",
        "options": {
            "fast": {
                "label": "Fast",
                "description": "Reduced accuracy for quick results",
            },
            "moderate": {
                "label": "Moderate",
                "description": "Balanced accuracy and performance",
            },
            "precise": {
                "label": "Precise",
                "description": "High accuracy for demanding calculations",
            },
        },
    },
}


@solara.component
def BasicSettings(data_model: solara.Reactive[QeDataModel]):
    calculation_parameters = data_model.fields.data.calculation_parameters
    basic_settings = calculation_parameters.basic
    system_settings = calculation_parameters.advanced.pw.parameters.SYSTEM

    REFS: dict[str, solara.Reactive] = {
        "electronic_type": Ref(basic_settings.electronic_type),
        "spin_type": Ref(basic_settings.spin_type),
        "lspinorb": Ref(system_settings.lspinorb),
        "noncolin": Ref(system_settings.noncolin),
        "nspin": Ref(system_settings.nspin),
        "protocol": Ref(basic_settings.protocol),
    }
    REFS |= {
        "spin_orbit": solara.use_reactive(
            "soc" if REFS["lspinorb"].value else "wo_soc"
        ),
    }

    def update_spin_orbit_parameters():
        spin_orbit = REFS["spin_orbit"]
        REFS["lspinorb"].set(spin_orbit.value == "soc")
        REFS["noncolin"].set(spin_orbit.value == "soc")
        REFS["nspin"].set(4 if spin_orbit.value == "soc" else 1)

    def Control(
        control: str,
        on_value: t.Callable | None = None,
        classes: list[str] | None = None,
    ):
        with solara.Row(classes=["control"]):
            solara.Text(
                f"{CONTROLS[control]['label']}:",
                classes=["control-label"],
            )
            with solara.ToggleButtonsSingle(
                value=REFS[control],
                on_value=on_value,
                dense=True,
                classes=classes or [],
            ):
                options: dict = CONTROLS[control]["options"]
                for option, data in options.items():
                    solara.Button(
                        label=data["label"],
                        tooltip=data["description"],
                        value=option,
                        style="width: 100px;",
                    )

    with solara.Div(class_="basic-settings"):
        Control("electronic_type")
        Control("spin_type")
        Control("spin_orbit", on_value=lambda _: update_spin_orbit_parameters())
        Control("protocol", classes=["protocol-selector"])
