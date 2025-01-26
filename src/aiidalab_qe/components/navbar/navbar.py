from aiidalab_qe.config.paths import STYLES
import solara
from solara.alias import rv


@solara.component
def QeNavBar():
    with rv.AppBar(color="secondary", dark=True):
        with rv.Container(class_="d-none"):
            with solara.Head():
                solara.Style(STYLES / "navbar.css")
        with rv.ToolbarTitle():
            with rv.Container(class_="d-flex p-0 align-center"):
                with solara.Link("aiidalab-qe"):
                    rv.Img(
                        class_="me-3",
                        src="https://aiidalab-qe.readthedocs.io/_images/icon.svg",
                        alt="The AiiDAlab Quantum ESPRESSO app",
                        width=40,
                    )
                rv.Text(
                    class_="appbar-title",
                    children=["The AiiDAlab Quantum ESPRESSO app"],
                )

        rv.Spacer()

        with solara.Link("aiidalab-qe"):
            rv.Btn(class_="px-2", text=True, children=["home"])
        with solara.Link("aiidalab-qe/workbench"):
            rv.Btn(class_="px-2", text=True, children=["workbench"])
        with solara.Link("aiidalab-qe/history"):
            rv.Btn(class_="px-2", text=True, children=["history"])
        with solara.Link("aiidalab-qe/resources"):
            rv.Btn(class_="px-2", text=True, children=["resources"])
