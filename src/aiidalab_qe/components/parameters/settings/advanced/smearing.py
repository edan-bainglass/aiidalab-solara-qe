from __future__ import annotations

import solara
from aiida_quantumespresso.workflows.pw.base import PwBaseWorkChain
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import (
    CalculationParametersModel,
    SystemParametersModel,
)
from aiidalab_qe.common.types import StructureType


@solara.component
def SmearingSettings(
    active: bool,
    input_structure: solara.Reactive[StructureType],
    parameters: solara.Reactive[CalculationParametersModel],
):
    protocol = Ref(parameters.fields.basic.protocol)
    smearing = Ref(parameters.fields.advanced.pw.parameters.SYSTEM.smearing)
    degauss = Ref(parameters.fields.advanced.pw.parameters.SYSTEM.degauss)

    def update_degauss():
        params = PwBaseWorkChain.get_protocol_inputs(protocol.value)
        system_params = params.get("pw", {}).get("parameters", {}).get("SYSTEM", {})
        smearing.set(system_params["smearing"])
        degauss.set(system_params["degauss"])

    solara.use_effect(
        update_degauss,
        [protocol.value],
    )

    with solara.Div(
        class_=" ".join(
            [
                "control-group smearing-settings",
                *(["d-none"] if not active else []),
            ],
        ),
    ):
        if not active:
            return

        print("\nrendering smearing-settings component")

        solara.Select(
            label="Smearing",
            values=[*SystemParametersModel.get_options("smearing")],
            value=smearing,
            on_value=smearing.set,
        )
        solara.InputFloat(
            label="degauss (Ry)",
            value=degauss,
        )
