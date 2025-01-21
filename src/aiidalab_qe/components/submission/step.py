from __future__ import annotations

import solara

from aiidalab_qe.common.models.schema import QeAppModel

from aiidalab_qe.common.components.wizard.step import onStateChange


@solara.component
def SubmissionStep(model: QeAppModel, on_state_change: onStateChange):
    pass
