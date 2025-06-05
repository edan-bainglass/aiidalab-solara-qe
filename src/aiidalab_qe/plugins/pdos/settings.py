from __future__ import annotations

import typing as t

import solara
import solara.toestand
from aiida_quantumespresso.workflows.pdos import PdosWorkChain

from aiidalab_qe.common.components.html import Paragraph
from aiidalab_qe.utils import create_kpoints_from_distance

from .model import PdosSettingsModel as Model

if t.TYPE_CHECKING:
    from aiidalab_qe.components.wizard.models import QeWizardModel


@solara.component
def PdosSettings(model: solara.Reactive[QeWizardModel]):
    calculation_parameters = model.fields.data.calculation_parameters
    protocol = solara.toestand.Ref(calculation_parameters.basic.protocol)
    input_structure = solara.toestand.Ref(model.fields.data.input_structure)

    pdos_settings: Model = calculation_parameters.plugins["pdos"].model  # type: ignore
    kpoints_distance = solara.toestand.Ref(pdos_settings.kpoints_distance)
    use_pdos_degauss = solara.toestand.Ref(pdos_settings.use_pdos_degauss)
    pdos_degauss = solara.toestand.Ref(pdos_settings.pdos_degauss)
    energy_grid_step = solara.toestand.Ref(pdos_settings.energy_grid_step)
    mesh_grid = solara.use_reactive("")
    degauss_ev = solara.use_reactive("")

    def update_mesh_grid():
        # TODO pbc guard is not correct. Address the underlying issue!
        if not (input_structure.value and any(input_structure.value.pbc)):
            grid = ""
        elif kpoints_distance.value > 0:
            mesh = create_kpoints_from_distance(
                input_structure.value,
                kpoints_distance.value,
                False,
            )
            grid = f"Mesh {mesh!s}"
        else:
            grid = "Please select a number higher than 0.0"
        mesh_grid.set(grid)

    solara.use_effect(
        update_mesh_grid,
        [kpoints_distance.value],
    )

    def update_degauss_ev():
        degauss_ev.set("({:.3f} eV)".format(pdos_degauss.value * 13.605698066))

    solara.use_effect(
        update_degauss_ev,
        [pdos_degauss.value],
    )

    def update_kpoints_distance():
        parameters = PdosWorkChain.get_protocol_inputs(protocol.value)
        if any(input_structure.value.pbc):
            distance = parameters["nscf"]["kpoints_distance"]
        else:
            distance = 100.0
            use_pdos_degauss.set(True)
        kpoints_distance.set(distance)

    solara.use_effect(
        update_kpoints_distance,
        [protocol.value],
    )

    with solara.Div(class_="pdos-settings"):
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
        with solara.Div(class_="plugin-controls"):
            with solara.HBox(classes=["align-items-baseline"]):
                solara.InputFloat(
                    label="NSCF K-points distance (Å⁻¹)",
                    value=kpoints_distance,
                )
                solara.Text(mesh_grid.value)
            solara.InputFloat(
                label="Energy grid step (eV)",
                value=energy_grid_step,
            )
            solara.Checkbox(
                label="Use custom PDOS degauss",
                value=use_pdos_degauss,
            )
            with solara.HBox():
                solara.InputFloat(
                    label="PDOS degauss (Ry)",
                    value=pdos_degauss,
                    disabled=not use_pdos_degauss.value,
                )
                solara.Text(degauss_ev.value)
