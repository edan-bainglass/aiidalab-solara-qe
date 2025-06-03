import typing as t

import solara

from aiidalab_qe.common.components.wizard.models import WizardModel
from aiidalab_qe.common.components.wizard.state import WizardState

onStateChange = t.Callable[[WizardState], None]
WizardStepType = t.Callable[
    [
        solara.Reactive[WizardModel],
        onStateChange,
    ],
    solara.Element,
]


class WizardStepConfirmButtonProps(t.TypedDict):
    label: str
    icon: str


class WizardStepProps(t.TypedDict):
    title: str
    component: WizardStepType
    confirm_button_props: WizardStepConfirmButtonProps
