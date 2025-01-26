import solara

from aiidalab_qe.config.paths import STYLES


@solara.component
def QeNavBar():
    with solara.v.AppBar(color="secondary", dark=True):
        with solara.v.Container(class_="d-none"):
            with solara.Head():
                solara.Style(STYLES / "navbar.css")
        with solara.v.ToolbarTitle():
            with solara.v.Container(class_="d-flex p-0 align-center"):
                with solara.Link("aiidalab-qe"):
                    solara.v.Img(
                        class_="me-3",
                        src="https://aiidalab-qe.readthedocs.io/_images/icon.svg",
                        alt="The AiiDAlab Quantum ESPRESSO app",
                        width=40,
                    )
                solara.v.Text(
                    class_="appbar-title",
                    children=["The AiiDAlab Quantum ESPRESSO app"],
                )

        solara.v.Spacer()

        with solara.Link("aiidalab-qe"):
            solara.v.Btn(class_="px-2", text=True, children=["home"])
        with solara.Link("aiidalab-qe/workbench"):
            solara.v.Btn(class_="px-2", text=True, children=["workbench"])
        with solara.Link("aiidalab-qe/history"):
            solara.v.Btn(class_="px-2", text=True, children=["history"])
        with solara.Link("aiidalab-qe/resources"):
            solara.v.Btn(class_="px-2", text=True, children=["resources"])
