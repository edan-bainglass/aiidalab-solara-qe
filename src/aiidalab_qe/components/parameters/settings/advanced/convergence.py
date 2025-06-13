from __future__ import annotations

import solara
from aiida import orm
from aiida_quantumespresso.workflows.pw.base import PwBaseWorkChain
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import CalculationParametersModel
from aiidalab_qe.utils import create_kpoints_from_distance


@solara.component
def ConvergenceSettings(
    input_structure: solara.Reactive[orm.StructureData],
    parameters: solara.Reactive[CalculationParametersModel],
):
    has_pbc = input_structure.value and any(input_structure.value.pbc)
    protocol = Ref(parameters.fields.basic.protocol)
    advanced_settings = parameters.fields.advanced
    forc_conv_thr = Ref(advanced_settings.pw.parameters.CONTROL.forc_conv_thr)
    etot_conv_thr = Ref(advanced_settings.pw.parameters.CONTROL.etot_conv_thr)
    scf_conv_thr = Ref(advanced_settings.pw.parameters.ELECTRONS.conv_thr)
    kpoints_distance = Ref(advanced_settings.kpoints_distance)
    mesh_grid = solara.use_reactive("")

    def update_mesh_grid():
        if not has_pbc:
            grid = ""
        elif kpoints_distance.value <= 0:
            grid = "Please select a number higher than 0.0"
        else:
            mesh = create_kpoints_from_distance(
                input_structure.value,
                kpoints_distance.value,
                False,
            )
            grid = f"{'x'.join([str(k) for k in mesh])} mesh"
        mesh_grid.set(grid)

    solara.use_effect(
        update_mesh_grid,
        [kpoints_distance.value, input_structure.value],
    )

    def update_from_protocol():
        params = PwBaseWorkChain.get_protocol_inputs(protocol.value)
        forc_conv_thr.set(params["pw"]["parameters"]["CONTROL"]["forc_conv_thr"])
        etot_conv_thr.set(params["meta_parameters"]["etot_conv_thr_per_atom"])
        scf_conv_thr.set(params["meta_parameters"]["conv_thr_per_atom"])
        kpoints_distance.set(params["kpoints_distance"] if has_pbc else 100.0)

    solara.use_effect(
        update_from_protocol,
        [protocol.value],
    )

    with solara.Div(class_="convergence-settings"):
        solara.InputFloat(
            label="Force (Ry/Bohr)",
            value=forc_conv_thr,
        )
        solara.InputFloat(
            label="Energy (Ry/atom)",
            value=etot_conv_thr,
        )
        solara.InputFloat(
            label="SCF (Ry/atom)",
            value=scf_conv_thr,
        )
        solara.InputFloat(
            label="Kpoints distance (Å⁻¹)",
            value=kpoints_distance,
        )
        solara.Text(mesh_grid.value)
