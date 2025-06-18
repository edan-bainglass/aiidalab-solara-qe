from __future__ import annotations

import solara
import solara.lab
import solara.toestand

from aiidalab_qe.common.components.wizard import onStateChange
from aiidalab_qe.common.types import ProcessType
from aiidalab_qe.components.results.structure import StructureResults
from aiidalab_qe.components.wizard.models import QeWizardModel
from aiidalab_qe.config.paths import STYLES
from aiidalab_qe.plugins.utils import get_plugin_results

plugin_results_panels = get_plugin_results()


@solara.component
def ResultsStep(
    model: solara.Reactive[QeWizardModel],
    on_state_change: onStateChange,
):
    process = solara.toestand.Ref(model.fields.data.process)

    if not process.value:
        solara.Info("No process found. Please submit a workflow.", classes=["mb-0"])
        return

    with solara.Head():
        solara.Style(STYLES / "results.css")

    with solara.Div(class_="results-step"):
        with solara.lab.Tabs(value=2):
            with solara.lab.Tab("Summary"):
                ProcessSummary(process.value)

            with solara.lab.Tab("Status"):
                ProcessStatus(process.value)

            with solara.lab.Tab("Results"):
                ProcessResults(process.value)


@solara.component
def ProcessSummary(process: ProcessType):
    with solara.Div(class_="process-panel summary-panel"):
        with solara.Column():
            solara.Text(f"pk: {process.pk}")
            solara.Text(f"Label: {process.label or 'No label'}")
            solara.Text(f"Description: {process.description or 'No description'}")


@solara.component
def ProcessStatus(process: ProcessType):
    with solara.Div(class_="process-panel status-panel"):
        solara.Text("Not yet implemented")


@solara.component
def ProcessResults(process: ProcessType):
    with solara.Div(class_="process-panel results-panel"):
        with solara.lab.Tabs():
            for prop in sorted(
                process.inputs.properties,
                key=lambda p: p != "relax",  # 'relax' should be first
            ):
                if prop == "pdos":
                    continue
                with solara.lab.Tab(prop):
                    with solara.Div(class_="results-view"):
                        if prop == "relax":
                            StructureResults(process)
                        elif prop in plugin_results_panels:
                            plugin_results_panels[prop]
