import typing as t

import solara

from aiidalab_qe.common.components.wizard.models import WDM
from aiidalab_qe.common.components.wizard.state import WizardState

onStateChange = t.Callable[[WizardState], None]
WizardStepType = t.Callable[
    [
        solara.Reactive[WDM],
        onStateChange,
    ],
    solara.Element,
]


class WizardStepProps(t.TypedDict):
    title: str
    component: WizardStepType
    is_submission_step: bool
