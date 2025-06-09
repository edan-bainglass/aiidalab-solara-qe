from __future__ import annotations

import typing as t

import solara
import solara.toestand
from aiida import orm
from ase.build import bulk, molecule

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.common.hooks import use_weas
from aiidalab_qe.config.paths import STYLES

from ..wizard.models import QeWizardModel

STRUCTURES = [
    "Bulk Si",
    "H2O molecule",
]


@solara.component
def StructureSelectionStep(
    model: solara.Reactive[QeWizardModel],
    on_state_change: onStateChange,
):
    print("\nrendering structure-selection-step component")

    process = solara.toestand.Ref(model.fields.data.process)
    input_structure = solara.toestand.Ref(model.fields.data.input_structure)
    selection = solara.use_reactive(t.cast(str, None))
    viewer = use_weas(input_structure.value)

    def select_structure(selected_structure: str):
        if selected_structure == "Bulk Si":
            new_structure = bulk("Si", "diamond", a=5.43)
        elif selected_structure == "H2O molecule":
            new_structure = molecule("H2O")
        if viewer.value:
            viewer.value.from_ase(new_structure)
        input_structure.set(orm.StructureData(ase=new_structure))

    def update_state():
        if not input_structure.value:
            new_state = WizardState.READY
        elif process.value:
            new_state = WizardState.SUCCESS
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
