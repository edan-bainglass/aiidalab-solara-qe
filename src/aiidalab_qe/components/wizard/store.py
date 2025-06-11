import typing as t

import solara

from aiidalab_qe.components.wizard.models import QeWizardModel


class WizardStore:
    def __init__(self):
        self.wizards = solara.reactive(
            t.cast(dict[str, solara.Reactive[QeWizardModel]], {})
        )
        self.active = solara.reactive(t.cast(int, None))

    def add_wizard(self, pk: t.Optional[int] = None):
        wizard = solara.reactive(QeWizardModel(pk=pk))
        new_uid = wizard.value.uid
        self.wizards.set({**self.wizards.value, new_uid: wizard})
        self.active.set(len(self.wizards.value) - 1)

    def remove_wizard(self, uid: str):
        wizards = self.wizards.value.copy()
        keys = list(wizards.keys())
        idx = keys.index(uid)
        del wizards[uid]
        self.wizards.set(wizards)
        if not (remaining := list(wizards.keys())):
            self.active.set(None)
        elif idx < len(remaining):
            self.active.set(idx)
        else:
            self.active.set(len(remaining) - 1)
