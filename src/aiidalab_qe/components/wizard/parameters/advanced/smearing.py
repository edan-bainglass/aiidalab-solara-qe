from __future__ import annotations

import solara
from aiida_quantumespresso.workflows.pw.base import PwBaseWorkChain
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import QeAppModel, SystemParametersModel


@solara.component
def SmearingSettings(active: bool, model: solara.Reactive[QeAppModel]):
    process = Ref(model.fields.process)
    parameters = model.fields.calculation_parameters
    protocol = Ref(parameters.basic.protocol)
    smearing = Ref(parameters.advanced.pw.parameters.SYSTEM.smearing)
    degauss = Ref(parameters.advanced.pw.parameters.SYSTEM.degauss)

    disabled = solara.use_memo(
        lambda: process.value is not None,
        [process.value],
    )

    def update_degauss():
        if disabled:
            return
        defaults = PwBaseWorkChain.get_protocol_inputs(protocol.value)
        smearing.set(defaults["pw"]["parameters"]["SYSTEM"]["smearing"])
        degauss.set(defaults["pw"]["parameters"]["SYSTEM"]["degauss"])

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
            disabled=disabled,
        )
        solara.InputFloat(
            label="degauss (Ry)",
            value=degauss,
            disabled=disabled,
        )
