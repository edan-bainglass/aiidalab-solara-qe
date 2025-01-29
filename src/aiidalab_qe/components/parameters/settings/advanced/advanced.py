from __future__ import annotations

import solara

from aiidalab_qe.components.wizard.models import QeDataModel


@solara.component
def AdvancedSettings(data_model: solara.Reactive[QeDataModel]):
    pass
