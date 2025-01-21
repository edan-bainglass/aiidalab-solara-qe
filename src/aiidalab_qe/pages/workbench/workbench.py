import solara
from solara.alias import rv

from aiidalab_qe.components.wizard import QeWizard


@solara.component
def Workbench():
    with rv.Container(class_="mt-2"):
        QeWizard()
