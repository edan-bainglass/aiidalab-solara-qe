import solara
from solara.alias import rv

from aiidalab_qe.common.components.header import Header
from aiidalab_qe.common.components.navbar import NavBar


@solara.component
def Home():
    print("\nrendering home page")
    with rv.Container(class_="mt-5"):
        Header(
            title="The AiiDAlab Quantum ESPRESSO app",
            subtitle="🎉 Happy computing 🎉",
            logo={
                "src": "https://aiidalab-qe.readthedocs.io/_images/icon.svg",
                "alt": "AiiDAlab Quantum ESPRESSO app logo",
            },
        )
        NavBar(
            [
                {
                    "label": "Getting started",
                    "icon": "rocket",
                },
                {
                    "label": "About",
                    "icon": "information",
                },
            ],
        )
