from __future__ import annotations

import solara
from aiida_quantumespresso.workflows.pw.base import PwBaseWorkChain
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.utils import create_kpoints_from_distance


@solara.component
def ConvergenceSettings(active: bool, model: solara.Reactive[QeAppModel]):
    process = Ref(model.fields.process)
    input_structure = Ref(model.fields.input_structure)
    has_pbc = input_structure.value and any(input_structure.value.pbc)
    parameters = model.fields.calculation_parameters
    protocol = Ref(parameters.basic.protocol)
    pw_parameters = parameters.advanced.pw.parameters
    forc_conv_thr = Ref(pw_parameters.CONTROL.forc_conv_thr)
    etot_conv_thr = Ref(pw_parameters.CONTROL.etot_conv_thr)
    scf_conv_thr = Ref(pw_parameters.ELECTRONS.conv_thr)
    kpoints_distance = Ref(parameters.advanced.kpoints_distance)

    disabled = solara.use_memo(
        lambda: process.value is not None,
        [process.value],
    )

    def get_mesh_grid():
        if not has_pbc:
            grid = "1x1x1 mesh (no PBC)"
        elif kpoints_distance.value <= 0:
            grid = "Please select a number higher than 0.0"
        else:
            mesh = create_kpoints_from_distance(
                input_structure.value,
                kpoints_distance.value,
                False,
            )
            grid = f"{'x'.join([str(k) for k in mesh])} mesh"
        return grid

    mesh_grid = solara.use_memo(
        get_mesh_grid,
        [input_structure.value, kpoints_distance.value],
    )

    protocol_defaults = solara.use_memo(
        PwBaseWorkChain.get_protocol_inputs,
        [protocol.value],
    )

    def update_convergence_criteria():
        if disabled:
            return
        defaults = protocol_defaults
        forc_conv_thr.set(defaults["pw"]["parameters"]["CONTROL"]["forc_conv_thr"])
        etot_conv_thr.set(defaults["meta_parameters"]["etot_conv_thr_per_atom"])
        scf_conv_thr.set(defaults["meta_parameters"]["conv_thr_per_atom"])

    def update_kpoints():
        if disabled:
            return
        defaults = protocol_defaults
        kpoints_distance.set(defaults["kpoints_distance"] if has_pbc else 100.0)

    solara.use_effect(
        update_convergence_criteria,
        [protocol.value],
    )

    solara.use_effect(
        update_kpoints,
        [input_structure.value, protocol.value],
    )

    with solara.Div(
        class_=" ".join(
            [
                "control-group convergence-settings",
                *(["d-none"] if not active else []),
            ],
        ),
    ):
        if not active:
            return

        print("\nrendering convergence-settings component")

        solara.InputFloat(
            label="Force (Ry/Bohr)",
            value=forc_conv_thr,
            disabled=disabled,
        )
        solara.InputFloat(
            label="Energy (Ry/atom)",
            value=etot_conv_thr,
            disabled=disabled,
        )
        solara.InputFloat(
            label="SCF (Ry/atom)",
            value=scf_conv_thr,
            disabled=disabled,
        )
        solara.InputFloat(
            label="Kpoints distance (Å⁻¹)",
            value=kpoints_distance,
            disabled=disabled or not has_pbc,
        )
        solara.Text(mesh_grid)
