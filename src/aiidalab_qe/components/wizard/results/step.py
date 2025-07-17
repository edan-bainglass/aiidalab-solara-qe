from __future__ import annotations

import solara
import solara.lab
from solara.toestand import Ref

from aiidalab_qe.common.components.wizard import onStateChange
from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.common.services.aiida import AiiDAService
from aiidalab_qe.config.paths import STYLES
from aiidalab_qe.plugins.utils import get_plugin_results

from .structure import StructureResults

plugin_results_panels = get_plugin_results()


@solara.component
def ResultsStep(
    model: solara.Reactive[QeAppModel],
    on_state_change: onStateChange,
):
    process = Ref(model.fields.process)

    if not process.value:
        solara.Info("No process found. Please submit a workflow.", classes=["mb-0"])
        return

    with solara.Head():
        solara.Style(STYLES / "results.css")

    with solara.Div(class_="results-step"):
        with solara.lab.Tabs(value=2):
            with solara.lab.Tab("Summary"):
                ProcessSummary(model)

            with solara.lab.Tab("Status"):
                ProcessStatus(model)

            with solara.lab.Tab("Results"):
                ProcessResults(model)


@solara.component
def ProcessSummary(model: solara.Reactive[QeAppModel]):
    process = Ref(model.fields.process)
    label = Ref(model.fields.label)
    description = Ref(model.fields.description)

    process_node = AiiDAService.load_process(process.value)

    with solara.Div(class_="process-panel summary-panel"):
        print("rendering process-summary component")

        with solara.Column():
            solara.HTML(
                "span",
                f"<b>PK:</b> {process_node.pk}",
            )
            solara.HTML(
                "span",
                f"<b>Label:</b> {label.value or 'No label'}",
            )
            solara.HTML(
                "span",
                f"<b>Description:</b> {description.value or 'No description'}",
            )


@solara.component
def ProcessStatus(model: solara.Reactive[QeAppModel]):
    process = Ref(model.fields.process)

    process_node = AiiDAService.load_process(process.value)

    with solara.Div(class_="process-panel status-panel"):
        print("rendering process-status component")

        solara.Text("Not yet implemented")


@solara.component
def ProcessResults(model: solara.Reactive[QeAppModel]):
    process = Ref(model.fields.process)

    process_node = AiiDAService.load_process(process.value)

    with solara.Div(class_="process-panel results-panel"):
        print("rendering process-results component")

        with solara.lab.Tabs():
            for prop in sorted(
                process_node.inputs.properties,
                key=lambda p: p != "relax",  # 'relax' should be first
            ):
                if prop == "pdos":
                    continue
                with solara.lab.Tab(prop):
                    with solara.Div(class_="results-view"):
                        if prop == "relax":
                            StructureResults(model)
                        elif prop in plugin_results_panels:
                            plugin_results_panels[prop]
