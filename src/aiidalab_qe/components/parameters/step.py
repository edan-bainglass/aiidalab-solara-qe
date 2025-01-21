from __future__ import annotations

from aiidalab_qe.common.models.schema import QeAppModel
import solara

from aiidalab_qe.common.components.wizard.step import onStateChange


@solara.component
def ParametersConfigurationStep(model: QeAppModel, on_state_change: onStateChange):
    pass
