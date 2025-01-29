from __future__ import annotations

import typing as t

import ase
import solara
from aiida import orm
from ase.build import bulk
from solara.toestand import Ref
from weas_widget import WeasWidget

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.config.paths import STYLES

from ..wizard.models import QeDataModel


@solara.component
def StructureSelectionStep(
    data_model: solara.Reactive[QeDataModel],
    on_state_change: onStateChange,
):
    print("rendering structure-selection-step component")
    input_structure = Ref(data_model.fields.data.input_structure)
    viewer, set_viewer = solara.use_state(t.cast(WeasWidget, None))
    structure, set_structure = solara.use_state(data_model.value.get_ase_structure())

    def initialize_viewer():
        if not viewer:
            weas = WeasWidget(viewerStyle={"width": "100%"})
            if structure:
                weas.from_ase(structure)
            set_viewer(weas)

    def update_structure(new_structure: ase.Atoms):
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

    with solara.v.Container(class_="structure-selection-step p-0"):
        if not viewer:
            with solara.v.Row(class_="text-center"):
                solara.SpinnerSolara()
        else:
            solara.Button(
                label="Select structure",
                color="primary",
                on_click=lambda: update_structure(bulk("Si", "diamond", a=5.43)),
            )
            with solara.v.Row():
                with solara.v.Col(lg=12, class_="pb-0"):
                    solara.v.Container(
                        class_="card",
                        children=[viewer],
                    )
