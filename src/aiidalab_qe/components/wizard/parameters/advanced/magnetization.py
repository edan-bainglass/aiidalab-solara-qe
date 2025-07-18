from __future__ import annotations

import solara
from aiida_pseudo.groups.family import PseudoPotentialFamily
from aiida_quantumespresso.workflows.protocols.utils import get_magnetization_parameters
from solara.toestand import Ref

from aiidalab_qe.common.components.selection import ToggleButtons
from aiidalab_qe.common.models.schema import MagneticMomentsType, QeAppModel
from aiidalab_qe.common.services.aiida import AiiDAService

DEFAULT_MOMENTS = get_magnetization_parameters()


@solara.component
def MagnetizationSettings(active: bool, model: solara.Reactive[QeAppModel]):
    process = Ref(model.fields.process)
    input_structure = Ref(model.fields.input_structure)
    spin_type = Ref(model.fields.calculation_parameters.basic.spin_type)
    advanced_settings = model.fields.calculation_parameters.advanced
    system_settings = advanced_settings.pw.parameters.SYSTEM
    pseudo_family = Ref(advanced_settings.pseudo_family)
    electronic_type = Ref(model.fields.calculation_parameters.basic.electronic_type)
    total_magnetization = Ref(system_settings.tot_magnetization)
    initial_magnetic_moments = Ref(advanced_settings.initial_magnetic_moments)

    input_type = solara.use_reactive(
        "moments" if electronic_type.value == "metal" else "total"
    )

    disabled = solara.use_memo(
        lambda: process.value is not None,
        [process.value],
    )

    def to_moment(
        symbol: str,
        family: PseudoPotentialFamily,
    ) -> float:
        moment = DEFAULT_MOMENTS.get(symbol, {}).get("magmom")
        return moment or round(0.1 * family.get_pseudo(symbol).z_valence, 3)

    def set_defaults():
        if disabled:
            return

        if not (
            spin_type.value == "collinear"
            and input_structure.value
            and (family := AiiDAService.load_pseudo_family(pseudo_family.value))
        ):
            total_magnetization.set(None)
            initial_magnetic_moments.set(None)
            return

        total_magnetization.set(0.0)
        initial_magnetic_moments.set(
            {
                kind.name: to_moment(kind.symbol, family)
                for kind in input_structure.value.kinds
            }
        )

    solara.use_effect(
        set_defaults,
        [input_structure.value, spin_type.value],
    )

    with solara.Div(
        class_=" ".join(
            [
                "control-group magnetization-settings",
                *(["d-none"] if not active else []),
            ],
        ),
    ):
        if not active:
            return

        print("rendering magnetization-settings component")

        if electronic_type.value == "metal":
            ToggleButtons(
                options={
                    "moments": {
                        "label": "Initial magnetic moments",
                    },
                    "total": {
                        "label": "Total magnetization",
                    },
                },
                value=input_type,
                disabled=disabled,
                class_="magnetization-input-selector",
            )
        # TODO hide div by settings `display` based on `active`
        MagneticMomentsInput(
            active=input_type.value == "moments",
            initial_magnetic_moments=initial_magnetic_moments,
            disabled=disabled,
        )
        TotalMagnetizationInput(
            active=input_type.value == "total",
            total_magnetization=total_magnetization,
            disabled=disabled,
        )


@solara.component
def TotalMagnetizationInput(
    active: bool,
    total_magnetization: solara.Reactive[float],
    disabled: bool = False,
):
    if active:
        with solara.Div(class_="total-magnetization-input"):
            solara.InputFloat(
                label="Total magnetization",
                value=total_magnetization,
                disabled=disabled,
            )


@solara.component
def MagneticMomentsInput(
    active: bool,
    initial_magnetic_moments: solara.Reactive[MagneticMomentsType],
    disabled: bool = False,
):
    if active:
        with solara.Div(class_="initial-magnetic-moments-input"):
            for site, moment in initial_magnetic_moments.value.items():

                def update_moments(value: float, site=site):
                    new_moments = initial_magnetic_moments.value.copy()
                    new_moments[site] = value
                    initial_magnetic_moments.set(new_moments)

                solara.InputFloat(
                    label=site,
                    value=moment,
                    on_value=update_moments,
                    disabled=disabled,
                )
