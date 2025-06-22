import typing as t

import solara

from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.components.wizard.models import QeWizardModel


class WizardStore:
    def __init__(self):
        self.wizards = solara.reactive(t.cast(list[solara.Reactive[QeWizardModel]], []))
        self.active = solara.reactive(t.cast(int, None))

    def add_wizard(self, pk: t.Optional[int] = None):
        wizard = solara.reactive(QeWizardModel(pk=pk))
        self.wizards.set([*self.wizards.value, wizard])
        self.active.set(len(self.wizards.value) - 1)
        self.active.set(len(self.wizards.value) - 1)

    def remove_wizard(self, index: int):
        wizards = self.wizards.value
        self.wizards.set([*wizards[:index], *wizards[index + 1 :]])
        if not len(self.wizards.value):
            self.active.set(None)
        elif index < len(self.wizards.value):
            self.active.set(index)
        else:
            self.active.set(len(self.wizards.value) - 1)
