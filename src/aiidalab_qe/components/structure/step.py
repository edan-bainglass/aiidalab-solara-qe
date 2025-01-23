from __future__ import annotations

import typing as t

import ase
import solara
from aiida import orm
from ase.build import bulk
from solara.alias import rv
from weas_widget import WeasWidget

from aiidalab_qe.common.components.wizard.state import State
from aiidalab_qe.common.components.wizard.step import onStateChange
from aiidalab_qe.common.config.paths import STYLES
from aiidalab_qe.components.wizard.models import WorkflowModel


@solara.component
def StructureSelectionStep(model: WorkflowModel, on_state_change: onStateChange):
    structure = solara.reactive(model.get_ase_structure())
    viewer = solara.reactive(t.cast(WeasWidget, None))

    def handle_structure(structure: ase.Atoms):
        structure.set(structure)
        if viewer.value:
            viewer.value.from_ase(structure)
        model.data.input_structure.set(orm.StructureData(ase=structure))

    def initialize_viewer():
        weas = WeasWidget(viewerStyle={"width": "100%"})
        if structure.value:
            weas.from_ase(structure.value)
        viewer.set(weas)

    solara.use_effect(
        lambda: on_state_change(State.CONFIGURED if structure.value else State.READY),
        [structure],
    )

    solara.use_effect(initialize_viewer, [])

    with solara.Head():
        solara.Style(STYLES / "structure.css")

    with rv.Container(class_=f"p-2 {'text-center' if not viewer.value else ''}"):
        if not viewer.value:
            solara.SpinnerSolara()
        else:
            solara.Button(
                label="Select structure",
                color="primary",
                on_click=lambda: handle_structure(bulk("Si", "diamond", a=5.43)),
            )
            with rv.Row():
                with rv.Col(lg=12, class_="pb-0"):
                    rv.Container(
                        class_="card border-secondary",
                        children=[viewer.value],
                    )
