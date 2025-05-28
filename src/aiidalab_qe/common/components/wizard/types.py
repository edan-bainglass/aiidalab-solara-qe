import typing as t

import solara

from aiidalab_qe.common.components.wizard.models import WizardDataModel
from aiidalab_qe.common.components.wizard.state import WizardState

onStateChange = t.Callable[[WizardState], None]
WizardStepType = t.Callable[
    [
        solara.Reactive[WizardDataModel],
        onStateChange,
    ],
    solara.Element,
]


class WizardStepProps(t.TypedDict):
    title: str
    component: WizardStepType
