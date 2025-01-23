from __future__ import annotations

import typing as t

import solara
from solara.alias import rv
from solara.lab import ConfirmationDialog, Tab, Tabs

from aiidalab_qe.common.config.paths import STYLES
from aiidalab_qe.components.wizard import QeWizard, WorkflowModel

# from aiidalab_qe.common.context import workbench_context


@solara.component
def Workbench():
    # workflows = solara.use_context(workbench_context)
    workflows = solara.use_reactive([WorkflowModel()])
    active_workflow = solara.use_reactive(t.cast(int, None))

    def add_workflow(pk: int | None = None):
        # workflows.append(WorkflowModel(pk))
        workflows.set([*workflows, WorkflowModel(pk=pk)])
        active_workflow.set(len(workflows))

    with rv.Container(class_="d-none"):
        with solara.Head():
            solara.Style(STYLES / "workbench.css")

    WorkbenchControls(add_workflow)

    with Tabs(
        vertical=True,
        lazy=True,
        value=active_workflow,
    ):
        for workflow in workflows.value:
            with Tab(tab_children=[TabHeader(workflow)]):
                with rv.Container(class_="workbench-body"):
                    QeWizard(workflow)


@solara.component
def TabHeader(workflow: WorkflowModel):
    with rv.Container(class_="d-flex p-0 align-items-center"):
        rv.Icon(
            children=[workflow.status_icon],
            class_="mr-1",
        )
        with rv.Col(
            class_="p-1 text-left",
            style_="max-width: 200px; overflow-x: clip; text-overflow: ellipsis;",
        ):
            if len(workflow.label) > 20:
                with solara.Tooltip(tooltip=workflow.label):
                    rv.Text(children=[workflow.label])
            else:
                rv.Text(children=[workflow.label])
        if workflow.pk.value:
            rv.Text(
                children=[f"[{workflow.pk.value}]"],
                class_="ml-auto",
            )


@solara.component
def WorkbenchControls(add_workflow: t.Callable[[int | None], None]):
    input_pk = solara.use_reactive(t.cast(int, None))
    active_dialog = solara.use_reactive(False)

    def prompt_for_pk():
        active_dialog.set(True)

    def on_prompt_submit():
        add_workflow(input_pk)
        input_pk.set(None)
        active_dialog.set(False)

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
        on_cancel=lambda: active_dialog.set(False),
        children=[
            rv.Row(
                children=[
                    solara.InputText(label="PK", value=input_pk),
                ],
            )
        ],
    )
