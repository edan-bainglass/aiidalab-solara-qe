from __future__ import annotations

import typing as t

import ase
import solara
import solara.toestand
from aiida import orm
from ase.build import bulk, molecule
from weas_widget import WeasWidget

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.config.paths import STYLES

from ..wizard.models import QeDataModel

STRUCTURES = [
    "Bulk Si",
    "H2O molecule",
]


def get_ase_structure(
    structure: t.Optional[orm.StructureData],
) -> t.Optional[ase.Atoms]:
    return structure.get_ase() if structure else None


@solara.component
def StructureSelectionStep(
    data_model: solara.Reactive[QeDataModel],
    on_state_change: onStateChange,
):
    print("\nrendering structure-selection-step component")

    input_structure = solara.toestand.Ref(data_model.fields.data.input_structure)
    selection = solara.use_reactive(t.cast(str, None))
    viewer = solara.use_reactive(t.cast(WeasWidget, None))
    structure = solara.use_reactive(get_ase_structure(input_structure.value))
    process = solara.toestand.Ref(data_model.fields.data.process)

    def initialize_viewer():
        if not viewer.value:
            weas: WeasWidget = WeasWidget(viewerStyle={"width": "100%"})
            if structure.value:
                weas.from_ase(structure.value)
            viewer.set(weas)

    def select_structure(selected_structure: str):
        if selected_structure == "Bulk Si":
            new_structure = bulk("Si", "diamond", a=5.43)
        elif selected_structure == "H2O molecule":
            new_structure = molecule("H2O")
        structure.set(new_structure)
        if viewer.value:
            viewer.value.from_ase(new_structure)
        input_structure.value = orm.StructureData(ase=new_structure)

    def update_state():
        if not input_structure.value:
            on_state_change(WizardState.READY)
        elif process.value:
            on_state_change(WizardState.SUCCESS)
        else:
            on_state_change(WizardState.CONFIGURED)

    solara.use_effect(initialize_viewer, [])

    solara.use_effect(update_state, [input_structure.value])

    with solara.Head():
        solara.Style(STYLES / "structure.css")

    with solara.Div(class_="structure-selection-step"):
        if not viewer.value:
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
                children=[viewer.value],
            )
