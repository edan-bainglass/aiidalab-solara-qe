from __future__ import annotations

import typing as t

import ase
import solara
from aiida import orm
from ase.build import bulk
from solara.alias import rv
from solara.toestand import Ref
from weas_widget import WeasWidget

from aiidalab_qe.common.components.wizard.state import State
from aiidalab_qe.common.components.wizard.step import onStateChange
from aiidalab_qe.common.config.paths import STYLES
from aiidalab_qe.components.wizard.models import WorkflowModel


@solara.component
def StructureSelectionStep(
    model: solara.Reactive[WorkflowModel],
    on_state_change: onStateChange,
):
    structure, set_structure = solara.use_state(model.value.get_ase_structure())
    viewer, set_viewer = solara.use_state(t.cast(WeasWidget, None))
    input_structure = Ref(model.fields.data.input_structure)

    def initialize_viewer():
        weas = WeasWidget(viewerStyle={"width": "100%"})
        if structure:
            weas.from_ase(structure)
        set_viewer(weas)

    def update_structure(new_structure: ase.Atoms):
        set_structure(new_structure)
        if viewer:
            viewer.from_ase(new_structure)
        input_structure.value = orm.StructureData(ase=new_structure)
        on_state_change(State.CONFIGURED)

    solara.use_effect(initialize_viewer, [])

    with solara.Head():
        solara.Style(STYLES / "structure.css")

    with rv.Container(class_=f"p-2 {'text-center' if not viewer else ''}"):
        if not viewer:
            solara.SpinnerSolara()
        else:
            solara.Button(
                label="Select structure",
                color="primary",
                on_click=lambda: update_structure(bulk("Si", "diamond", a=5.43)),
            )
            with rv.Row():
                with rv.Col(lg=12, class_="pb-0"):
                    rv.Container(
                        class_="card border-secondary",
                        children=[viewer],
                    )
