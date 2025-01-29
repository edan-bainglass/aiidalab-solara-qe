import solara

from aiidalab_qe.config.paths import STYLES


@solara.component
def QeNavBar(pages: dict):
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

        for page, page_data in pages.items():
            with solara.Link(page_data["link"]):
                solara.v.Btn(class_="px-2", text=True, children=[page])
