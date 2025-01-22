from __future__ import annotations

import typing as t
from dataclasses import dataclass
from enum import Enum

import solara
from aiida.engine import ProcessState
from solara.alias import rv
from solara.lab import ConfirmationDialog, Tab, Tabs

from aiidalab_qe.common.config.paths import STYLES
from aiidalab_qe.common.services.aiida import AiiDAService
from aiidalab_qe.components.wizard import QeWizard


class StatusIcon(Enum):
    CREATED = "\u25cb"
    WAITING = "\u25ce"
    RUNNING = "\u231b"
    FINISHED = "\u2713"
    EXCEPTED = "\u26a0"
    FAILED = "\u00d7"


@dataclass
class WorkflowModel:
    pk: int | None = None
    status: ProcessState | None = None

    @property
    def label(self) -> str:
        if self.pk:
            if process := AiiDAService.load_qe_app_workflow_node(self.pk):
                icon = StatusIcon[process.process_state.name].value
                return f"{icon} {process.label or 'Workflow'} [pk={self.pk}]"
        return "New workflow"


@solara.component
def Workbench():
    workflows, set_workflows = solara.use_state([WorkflowModel()])
    active_workflow, set_active_workflow = solara.use_state(t.cast(int, None))
    input_pk, set_input_pk = solara.use_state(t.cast(int, None))
    active_dialog, set_active_dialog = solara.use_state(False)

    def add_workflow(pk: int | None = None):
        set_workflows([*workflows, WorkflowModel(pk)])
        set_active_workflow(len(workflows))

    def prompt_for_pk():
        set_active_dialog(True)

    def on_prompt_submit():
        add_workflow(input_pk)
        set_input_pk(None)
        set_active_dialog(False)

    with rv.Col(class_="p-0"):
        with solara.Head():
            solara.Style(STYLES / "workbench.css")

        with rv.Row(class_="mx-2 my-0"):
            solara.Button(
                color="secondary",
                icon=True,
                icon_name="mdi-plus-thick",
                on_click=add_workflow,
            )
            solara.Button(
                color="secondary",
                icon=True,
                icon_name="mdi-key-plus",
                on_click=prompt_for_pk,
            )

        ConfirmationDialog(
            active_dialog,
            title="Enter workflow PK",
            ok="Submit",
            on_ok=lambda: on_prompt_submit(),
            on_cancel=lambda: set_active_dialog(False),
            children=[
                rv.Row(
                    children=[
                        solara.InputText(
                            label="PK",
                            value=input_pk,
                            on_value=set_input_pk,
                        )
                    ]
                )
            ],
        )

        with Tabs(
            vertical=True,
            lazy=True,
            value=active_workflow,
            on_value=set_active_workflow,
        ):
            for workflow in workflows:
                with Tab(label=workflow.label):
                    with rv.Container(class_="workbench-body overflow-y-auto"):
                        QeWizard(workflow.pk)
