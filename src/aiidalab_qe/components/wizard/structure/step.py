from __future__ import annotations

import typing as t

import ase.build
import solara
from aiida import orm
from ase.io import read
from solara.toestand import Ref

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.common.hooks import use_weas
from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.config.paths import DATA, STYLES

STRUCTURES = [
    "Bulk Si",
    "LiCoO2",
    "H2O molecule",
]


@solara.component
def StructureSelectionStep(
    model: solara.Reactive[QeAppModel],
    on_state_change: onStateChange,
):
    process = Ref(model.fields.process)
    input_structure = Ref(model.fields.input_structure)
    selection = solara.use_reactive(t.cast(str, None))
    viewer = use_weas(input_structure.value)

    disabled = solara.use_memo(
        lambda: process.value is not None,
        [process.value],
    )

    def select_structure(selected_structure: str):
        if selected_structure == "Bulk Si":
            new_structure = ase.build.bulk("Si", "diamond", a=5.43)
        elif selected_structure == "H2O molecule":
            new_structure = ase.build.molecule("H2O")
        else:
            path = DATA / "structure/examples" / selected_structure
            new_structure = read(path.with_suffix(".vasp"), format="vasp")
        if viewer.value:
            viewer.value.from_ase(new_structure)
        structure = orm.StructureData(ase=new_structure)
        structure.store()
        input_structure.set(structure)

    def update_state():
        if disabled:
            return

        if not input_structure.value:
            new_state = WizardState.READY
        else:
            new_state = WizardState.CONFIGURED

        on_state_change(new_state)

    solara.use_effect(
        update_state,
        [input_structure.value],
    )

    with solara.Head():
        solara.Style(STYLES / "structure.css")

    with solara.Div(class_="structure-selection-step"):
        print("rendering structure-selection-step component")

        if not viewer.value:
            with solara.Div(class_="spinner"):
                solara.SpinnerSolara()
        else:
            solara.Select(
                label="Select structure",
                value=selection,
                values=STRUCTURES,
                on_value=select_structure,
                disabled=disabled,
                classes=["structure-selector"],
            )
            solara.Div(
                class_="structure-viewer card",
                children=[viewer.value],
            )
