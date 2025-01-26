from __future__ import annotations

import solara

from aiidalab_qe.common.components.wizard.step import onStateChange
from aiidalab_qe.components.wizard.models import QeDataModel


@solara.component
def SubmissionStep(
    model: solara.Reactive[QeDataModel],
    on_state_change: onStateChange,
):
    pass
