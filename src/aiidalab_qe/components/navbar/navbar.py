import solara

from aiidalab_qe.config.paths import APP_URL_ROOT, STYLES


@solara.component
def QeNavBar(pages: dict):
    with solara.Head():
        solara.Style(STYLES / "navbar.css")

    with solara.v.AppBar(color="secondary", dark=True, class_="app-navbar"):
        with solara.v.ToolbarTitle(class_="toolbar"):
            with solara.Link(APP_URL_ROOT):
                solara.v.Img(
                    class_="me-3",
                    src="https://aiidalab-qe.readthedocs.io/_images/icon.svg",
                    alt="The AiiDAlab Quantum ESPRESSO app",
                    width=40,
                )
            solara.Text(
                "The AiiDAlab Quantum ESPRESSO app",
                classes=["appbar-title"],
            )

        solara.v.Spacer()

        for page, page_data in pages.items():
            with solara.Link(page_data["link"]):
                solara.v.Btn(class_="px-2", text=True, children=[page])
