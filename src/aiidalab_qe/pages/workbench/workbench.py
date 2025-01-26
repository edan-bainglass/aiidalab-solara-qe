from __future__ import annotations

import typing as t

import solara
from solara import lab
from solara.alias import rv

from aiidalab_qe.common.components.wizard import WizardModel
from aiidalab_qe.components.wizard import QeWizard
from aiidalab_qe.components.wizard.models import WorkflowDataModel
from aiidalab_qe.config.paths import STYLES

wizard_models = solara.reactive([solara.reactive(WizardModel())])
data_models = solara.reactive([solara.reactive(WorkflowDataModel())])

active = solara.reactive(t.cast(int, None))


@solara.component
def Workbench():
    print("\nrendering workbench page")

    def add_workflow(pk: int | None = None):
        wizard_models.set(
            [
                *wizard_models.value,
                solara.reactive(WizardModel(pk=pk)),
            ],
        )
        data_models.set(
            [
                *data_models.value,
                solara.reactive(WorkflowDataModel(pk=pk)),
            ],
        )
        active.set(len(data_models.value) - 1)

    def remove_workflow(index: int):
        wizard_models.set(
            [
                *wizard_models.value[:index],
                *wizard_models.value[index + 1 :],
            ],
        )
        data_models.set(
            [
                *data_models.value[:index],
                *data_models.value[index + 1 :],
            ],
        )
        active.set(len(data_models.value) - 1)

    with rv.Container(class_="d-none"):
        with solara.Head():
            solara.Style(STYLES / "workbench.css")

    WorkbenchControls(add_workflow=add_workflow)

    with lab.Tabs(
        vertical=True,
        lazy=True,
        value=active,
    ):
        for i, (data_model, wizard_model) in enumerate(
            zip(
                data_models.value,
                wizard_models.value,
            )
        ):
            with lab.Tab(
                tab_children=[
                    TabHeader(
                        data_model,
                        lambda i=i: remove_workflow(i),
                    ),
                ],
            ):
                with rv.Container(class_="workbench-body"):
                    QeWizard(wizard_model, data_model)


@solara.component
def TabHeader(workflow: solara.Reactive[WorkflowDataModel], remove_workflow):
    with rv.Container(class_="d-flex p-0 align-items-center"):
        # TODO stop close event propagation to tab selection (leads to index out of bound)
        solara.Button(
            color="error",
            icon_name="mdi-close",
            class_="mr-1 p-0 tab-close-button",
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
