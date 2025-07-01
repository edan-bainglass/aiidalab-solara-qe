import solara

from aiidalab_qe.common.components.header import Header
from aiidalab_qe.common.components.navbar import NavBar
from aiidalab_qe.config.paths import STYLES


@solara.component
def Home():
    print("rendering home page")

    with solara.Head():
        solara.Style(STYLES / "home.css")

    with solara.Div(class_="home container"):
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
                    "label": "Get started",
                    "icon": "rocket",
                },
                {
                    "label": "About",
                    "icon": "information",
                },
            ],
        )
