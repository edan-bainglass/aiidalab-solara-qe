from __future__ import annotations

import solara

from aiidalab_qe.common.components.wizard import onStateChange
from aiidalab_qe.components.wizard.models import QeWizardModel


@solara.component
def ResultsStep(
    model: solara.Reactive[QeWizardModel],
    on_state_change: onStateChange,
):
    pass
