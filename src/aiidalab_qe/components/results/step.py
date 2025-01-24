from __future__ import annotations

import solara

from aiidalab_qe.common.components.wizard.step import onStateChange
from aiidalab_qe.components.wizard.models import WorkflowModel


@solara.component
def ResultsStep(
    model: solara.Reactive[WorkflowModel],
    on_state_change: onStateChange,
):
    pass
