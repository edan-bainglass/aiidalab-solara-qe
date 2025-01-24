from __future__ import annotations

import typing as t

import solara
from solara import lab
from solara.alias import rv

from aiidalab_qe.common.config.paths import STYLES
from aiidalab_qe.components.wizard import QeWizard, WorkflowModel

workflows = solara.reactive([solara.reactive(WorkflowModel())])
active_workflow = solara.reactive(t.cast(int, None))


@solara.component
def Workbench():
    def add_workflow(pk: int | None = None):
        workflows.set([*workflows.value, solara.reactive(WorkflowModel(pk=pk))])
        active_workflow.set(len(workflows.value) - 1)

    def remove_workflow(index: int):
        workflows.set([*workflows.value[:index], *workflows.value[index + 1 :]])
        active_workflow.set(len(workflows.value) - 1)

    with rv.Container(class_="d-none"):
        with solara.Head():
            solara.Style(STYLES / "workbench.css")

    WorkbenchControls(add_workflow=add_workflow)

    with lab.Tabs(
        vertical=True,
        lazy=True,
        value=active_workflow,
    ):
        for i, workflow in enumerate(workflows.value):
            with lab.Tab(
                tab_children=[
                    TabHeader(
                        workflow,
                        lambda i=i: remove_workflow(i),
                    )
                ]
            ):
                with rv.Container(class_="workbench-body"):
                    QeWizard(workflow)


@solara.component
def TabHeader(workflow: solara.Reactive[WorkflowModel], remove_workflow):
    with rv.Container(class_="d-flex p-0 align-items-center"):
        # TODO stop close event propagation to tab selection
        solara.Button(
            color="error",
            icon_name="mdi-close",
            class_="mr-1 p-0",
            style_="min-width: unset;",
            text=True,
            on_click=remove_workflow,
        )
        rv.Icon(
            children=[workflow.value.status_icon],
            class_="mr-1",
        )
        with rv.Col(
            class_="p-1 text-left",
            style_="max-width: 200px; overflow-x: clip; text-overflow: ellipsis;",
        ):
            if len(workflow.value.label) > 20:
                with solara.Tooltip(tooltip=workflow.value.label):
                    rv.Text(children=[workflow.value.label])
            else:
                rv.Text(children=[workflow.value.label])
        if workflow.value.pk:
            rv.Text(
                children=[f"[{workflow.value.pk}]"],
                class_="ml-auto",
            )


@solara.component
def WorkbenchControls(add_workflow: t.Callable[[int | None], None]):
    input_pk, set_input_pk = solara.use_state(t.cast(int, None))
    active_dialog, set_active_dialog = solara.use_state(False)

    def prompt_for_pk():
        set_active_dialog(True)

    def on_prompt_submit():
        add_workflow(input_pk)
        set_input_pk(0)
        set_active_dialog(False)

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

    lab.ConfirmationDialog(
        active_dialog,
        title="Enter workflow PK",
        ok="Submit",
        on_ok=lambda: on_prompt_submit(),
        on_cancel=lambda: set_active_dialog(False),
        children=[
            rv.Row(
                children=[
                    solara.InputInt(
                        label="PK",
                        value=input_pk,
                        on_value=set_input_pk,
                        autofocus=True,
                    ),
                ],
            )
        ],
    )
