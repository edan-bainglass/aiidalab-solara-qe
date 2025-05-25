from __future__ import annotations

import typing as t

import solara
from aiida import orm
from ase.build import bulk, molecule
from solara.toestand import Ref
from weas_widget import WeasWidget

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.config.paths import STYLES

from ..wizard.models import QeDataModel

STRUCTURES = [
    "Bulk Si",
    "H2O molecule",
]


@solara.component
def StructureSelectionStep(
    data_model: solara.Reactive[QeDataModel],
    on_state_change: onStateChange,
):
    print("\nrendering structure-selection-step component")
    input_structure = Ref(data_model.fields.data.input_structure)
    selection = solara.use_reactive(t.cast(str, None))
    viewer, set_viewer = solara.use_state(t.cast(WeasWidget, None))
    structure, set_structure = solara.use_state(data_model.value.get_ase_structure())

    def initialize_viewer():
        if not viewer:
            weas: WeasWidget = WeasWidget(viewerStyle={"width": "100%"})
            if structure:
                weas.from_ase(structure)
            set_viewer(weas)

    def select_structure(selected_structure: str):
        if selected_structure == "Bulk Si":
            new_structure = bulk("Si", "diamond", a=5.43)
        elif selected_structure == "H2O molecule":
            new_structure = molecule("H2O")
        set_structure(new_structure)
        if viewer:
            viewer.from_ase(new_structure)
        input_structure.value = orm.StructureData(ase=new_structure)

    solara.use_effect(initialize_viewer, [])

    solara.use_effect(
        lambda: input_structure.value and on_state_change(WizardState.CONFIGURED),
        [input_structure.value],
    )

    with solara.Head():
        solara.Style(STYLES / "structure.css")

    with solara.Div(class_="structure-selection-step"):
        if not viewer:
            with solara.Div(class_="spinner"):
                solara.SpinnerSolara()
        else:
            solara.Select(
                label="Select structure",
                value=selection,
                values=STRUCTURES,
                on_value=select_structure,
                classes=["structure-selector"],
            )
            solara.Div(
                class_="structure-viewer card",
                children=[viewer],
            )
