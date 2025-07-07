import solara

from aiidalab_qe.config.deployment import get_root_path
from aiidalab_qe.config.paths import STYLES


@solara.component
def QeNavBar(pages: dict):
    with solara.Head():
        solara.Style(STYLES / "navbar.css")

    with solara.v.AppBar(color="secondary", dark=True, class_="app-navbar"):
        with solara.v.ToolbarTitle(class_="toolbar"):
            with solara.Link(f"{get_root_path()}/"):
                solara.Image(
                    image="https://aiidalab-qe.readthedocs.io/_images/icon.svg",
                    width="40px",
                    classes=["me-3"],
                )
            solara.Text(
                "The AiiDAlab Quantum ESPRESSO app",
                classes=["appbar-title"],
            )

        solara.v.Spacer()

        for page, page_data in pages.items():
            with solara.Link(page_data["link"]):
                solara.v.Btn(class_="px-2", text=True, children=[page])
