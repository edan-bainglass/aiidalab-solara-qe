from __future__ import annotations

import typing as t

import solara
import solara.toestand
from aiida_quantumespresso.workflows.pdos import PdosWorkChain

from aiidalab_qe.common.components.html import Paragraph
from aiidalab_qe.common.models.schema import CalculationParametersModel
from aiidalab_qe.common.types import StructureType
from aiidalab_qe.utils import create_kpoints_from_distance

from .model import PdosSettingsModel as Model


@solara.component
def PdosSettings(
    active: bool,
    input_structure: solara.Reactive[StructureType],
    parameters: solara.Reactive[CalculationParametersModel],
):
    has_pbc = input_structure.value and any(input_structure.value.pbc)
    protocol = solara.toestand.Ref(parameters.fields.basic.protocol)
    pdos_settings = t.cast(Model, parameters.fields.plugins["pdos"].model)
    kpoints_distance = solara.toestand.Ref(pdos_settings.kpoints_distance)
    use_pdos_degauss = solara.toestand.Ref(pdos_settings.use_pdos_degauss)
    pdos_degauss = solara.toestand.Ref(pdos_settings.pdos_degauss)
    energy_grid_step = solara.toestand.Ref(pdos_settings.energy_grid_step)

    degauss_ev = solara.use_memo(
        lambda: "({:.3f} eV)".format(pdos_degauss.value * 13.605698066),
        [pdos_degauss.value],
    )

    def get_mesh_grid():
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

        return grid

    mesh_grid = solara.use_memo(
        get_mesh_grid,
        [input_structure.value, kpoints_distance.value],
    )

    protocol_defaults = solara.use_memo(
        PdosWorkChain.get_protocol_inputs,
        [protocol.value],
    )

    def update_kpoints_distance():
        defaults = protocol_defaults
        if has_pbc:
            distance = defaults["nscf"]["kpoints_distance"]
        else:
            distance = 100.0
            use_pdos_degauss.set(True)
        kpoints_distance.set(distance)

    solara.use_effect(
        update_kpoints_distance,
        [input_structure.value, protocol.value],
    )

    with solara.Div(
        class_=" ".join(
            [
                "control-group pdos-settings",
                *(["d-none"] if not active else []),
            ],
        ),
    ):
        if not active:
            return

        print("\nrendering pdos-settings component")

        with solara.Div(class_="plugin-info"):
            Paragraph("""
                By default, the <b>tetrahedron method</b> is used for the partial
                density of states (PDOS) calculation. However, if you need more control
                over the broadening, you can apply <b>Gaussian broadening</b> by
                specifying a custom <b>degauss</b> value.
            """)
            Paragraph("""
                For systems involving <b>molecules</b> or <b>localized orbitals</b>, it
                is recommended to use a <b>custom degauss value</b>. This will provide
                a more accurate representation of the PDOS, especially when the
                electronic states are localized.
            """)

        solara.InputFloat(
            label="NSCF K-points distance (Å⁻¹)",
            value=kpoints_distance,
        )
        solara.Text(mesh_grid)

        solara.InputFloat(
            label="Energy grid step (eV)",
            value=energy_grid_step,
        )

        solara.Checkbox(
            label="Use custom PDOS degauss",
            value=use_pdos_degauss,
        )

        solara.InputFloat(
            label="PDOS degauss (Ry)",
            value=pdos_degauss,
            disabled=not use_pdos_degauss.value,
        )
        solara.Text(degauss_ev)
