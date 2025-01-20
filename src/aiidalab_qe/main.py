from __future__ import annotations

from aiidalab_qe.components.header import Header
from aiidalab_qe.components.navbar import NavBar
import solara
from aiida import load_profile
from solara.alias import rv

from aiidalab_qe.common.context import qe_context
from aiidalab_qe.common.paths import STYLES
from aiidalab_qe.common.schema import QeAppModel
from aiidalab_qe.components import (
    ParameterConfigurationStep,
    ResourcesSelectionStep,
    ResultsStep,
    StructureSelectionStep,
    SubmissionStep,
    Wizard,
)

_ = load_profile()


@solara.component
def Layout(children=[]):
    AppNavBar()
    rv.Container(class_="my-5", children=children)


@solara.component
def AppNavBar():
    with rv.AppBar(color="secondary", dark=True):
        with solara.Head():
            solara.Title("AiiDAlab QE app")
            solara.Style(STYLES / "main.css")

        with rv.ToolbarTitle():
            with rv.Container(class_="d-flex align-center"):
                with solara.Link("aiidalab-qe"):
                    rv.Img(
                        class_="me-3",
                        src="https://aiidalab-qe.readthedocs.io/_images/icon.svg",
                        alt="The AiiDAlab Quantum ESPRESSO app",
                        width=40,
                    )
                rv.Text(children=["The AiiDAlab Quantum ESPRESSO app"])

        rv.Spacer()

        with solara.Link("aiidalab-qe"):
            rv.Btn(text=True, children=["home"])
        with solara.Link("aiidalab-qe/workbench"):
            rv.Btn(text=True, children=["workbench"])
        with solara.Link("aiidalab-qe/history"):
            rv.Btn(text=True, children=["history"])
        with solara.Link("aiidalab-qe/resources"):
            rv.Btn(text=True, children=["resources"])


@solara.component
def Home():
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
            {
                "label": "Calculation history",
                "icon": "format-list-bulleted-square",
                "href": "",
            },
            {
                "label": "Setup resources",
                "icon": "database",
                "href": "",
            },
            {
                "label": "New calculation",
                "icon": "plus-circle",
                "href": "",
            },
        ],
    )


@solara.component
def Workbench():
    router = solara.use_router()

    rv.Html(tag="h1", children=["Workbench"])
    Wizard(
        steps=[
            {
                "title": "Select structure",
                "component": StructureSelectionStep,
            },
            {
                "title": "Configure the workflow",
                "component": ParameterConfigurationStep,
            },
            {
                "title": "Choose computational resources",
                "component": ResourcesSelectionStep,
            },
            {
                "title": "Submit the workflow",
                "component": SubmissionStep,
            },
            {
                "title": "Status & results",
                "component": ResultsStep,
            },
        ],
        context=qe_context,
        defaults=QeAppModel(
            input_structure=None,
            calculation_parameters={},
            computational_resources={},
            process=router.search.split("pk=")[-1] if router.search else None,
        ),
    )


@solara.component
def CalculationHistory():
    rv.Html(tag="h1", children=["Calculation history"])


@solara.component
def ResourceSetup():
    rv.Html(tag="h1", children=["Resource setup"])


routes = [
    solara.Route(
        path="aiidalab-qe",
        children=[
            solara.Route(path="/", component=Home),
            solara.Route(path="workbench", component=Workbench),
            solara.Route(path="history", component=CalculationHistory),
            solara.Route(path="resources", component=ResourceSetup),
        ],
        layout=Layout,
    ),
]
