from __future__ import annotations

import typing as t

import ase
import solara
from aiida import orm
from ase.build import bulk
from solara.alias import rv
from weas_widget import WeasWidget

from aiidalab_qe.common.context import qe_context
from aiidalab_qe.common.paths import STYLES
from aiidalab_qe.common.state import State

from ..wizard.step import onStateChange


@solara.component
def StructureSelectionStep(on_state_change: onStateChange):
    context = solara.use_context(qe_context)
    structure, set_structure = solara.use_state(t.cast(ase.Atoms, None))
    viewer, set_viewer = solara.use_state(t.cast(WeasWidget, None))

    def handle_structure(structure: ase.Atoms):
        set_structure(structure)
        if viewer:
            viewer.from_ase(structure)
        context.input_structure = orm.StructureData(ase=structure)

    def initialize_viewer():
        set_viewer(WeasWidget(viewerStyle={"width": "100%"}))

    solara.use_effect(
        lambda: on_state_change(State.CONFIGURED if structure else State.READY),
        [structure],
    )

    solara.use_effect(lambda: not viewer and initialize_viewer(), [])

    with solara.Head():
        solara.Style(STYLES / "structure.css")

    with rv.Container(class_=f"p-2 {'text-center' if not viewer else ''}"):
        if not viewer:
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
                        children=[viewer],
                    )
