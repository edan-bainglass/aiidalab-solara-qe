from __future__ import annotations

import solara
from aiida import load_profile

from aiidalab_qe.common.context import qe_context
from aiidalab_qe.common.paths import STYLES
from aiidalab_qe.common.schema import QeAppModel
from aiidalab_qe.components import (
    App,
    ParameterConfigurationStep,
    ResourcesSelectionStep,
    ResultsStep,
    StructureSelectionStep,
    SubmissionStep,
    Wizard,
)

_ = load_profile()


@solara.component
def Page():
    with solara.Head():
        solara.Title("AiiDAlab QE app")
        solara.Style(STYLES / "main.css")

    with App(
        title="The AiiDAlab Quantum ESPRESSO app",
        subtitle="🎉 Happy computing 🎉",
        logo={
            "src": "https://aiidalab-qe.readthedocs.io/_images/icon.svg",
            "alt": "AiiDAlab Quantum ESPRESSO app logo",
        },
        nav_items=[
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
    ):
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
                process=None,
            ),
        )


if __name__ == "__main__":
    Page()
