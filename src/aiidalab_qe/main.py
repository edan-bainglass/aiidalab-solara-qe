from __future__ import annotations

from pathlib import Path

import solara

from aiida import load_profile
from aiidalab_qe.components import (
    ParameterConfigurationStep,
    ResourcesSelectionStep,
    ResultsStep,
    StructureSelectionStep,
    SubmissionStep,
    WizardApp,
)

_ = load_profile()

ROOT = Path(__file__).parent


@solara.component
def Page():
    with solara.Head():
        solara.Title("AiiDAlab QE app")
        solara.Style(ROOT / "assets/styles/css/main.css")
    WizardApp(
        title="The AiiDAlab Quantum ESPRESSO app",
        subtitle="🎉 Happy computing 🎉",
        logo={
            "src": ROOT / "assets/images/aiidalab_qe_logo.png",
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
        steps=[
            (
                "Select structure",
                StructureSelectionStep,
            ),
            (
                "Configure the workflow",
                ParameterConfigurationStep,
            ),
            (
                "Choose computational resources",
                ResourcesSelectionStep,
            ),
            (
                "Submit the workflow",
                SubmissionStep,
            ),
            (
                "Status & results",
                ResultsStep,
            ),
        ],
    )
