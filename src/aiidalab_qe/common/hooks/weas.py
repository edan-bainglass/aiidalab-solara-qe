import typing as t

import ase
import solara
from weas_widget import WeasWidget

from aiidalab_qe.common.types import StructureType


def get_ase_structure(structure: StructureType) -> t.Optional[ase.Atoms]:
    return structure.get_ase() if structure else None


def use_weas(structure: StructureType) -> solara.Reactive[t.Optional[WeasWidget]]:
    viewer = solara.use_reactive(t.cast(t.Optional[WeasWidget], None))

    def initialize_viewer():
        if not viewer.value:
            widget: WeasWidget = WeasWidget(
                viewerLayout={
                    "width": "100%",
                    "height": "100%",
                }
            )
            if structure:
                widget.from_ase(get_ase_structure(structure))
            viewer.set(widget)

    solara.use_effect(
        initialize_viewer,
        [],
    )

    return viewer
