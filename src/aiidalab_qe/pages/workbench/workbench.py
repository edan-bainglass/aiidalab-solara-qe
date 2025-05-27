from __future__ import annotations

import typing as t

import solara
import solara.lab

from aiidalab_qe.components.wizard import QeWizard
from aiidalab_qe.components.wizard.models import QeDataModel, QeWizardModel
from aiidalab_qe.config.paths import STYLES

wizard_models = solara.reactive([solara.reactive(QeWizardModel())])
data_models = solara.reactive([solara.reactive(QeDataModel())])

active = solara.reactive(t.cast(int, None))


@solara.component
def Workbench():
    print("\n" * 5 + "rendering workbench page")

    def add_workflow(pk: int | None = None):
        wizard_models.set(
            [
                *wizard_models.value,
                solara.reactive(QeWizardModel(pk=pk)),
            ],
        )
        data_models.set(
            [
                *data_models.value,
                solara.reactive(QeDataModel(pk=pk)),
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

    with solara.Head():
        solara.Style(STYLES / "workbench.css")

    with solara.Div(class_="workbench"):
        WorkbenchControls(add_workflow=add_workflow)
        with solara.lab.Tabs(
            vertical=True,
            lazy=False,
            value=active,
        ):
            for i, (data_model, wizard_model) in enumerate(
                zip(
                    data_models.value,
                    wizard_models.value,
                )
            ):
                with solara.lab.Tab(
                    tab_children=[
                        TabHeader(
                            data_model,
                            lambda i=i: remove_workflow(i),
                        ),
                    ],
                ):
                    with solara.Div(class_="workbench-body container"):
                        QeWizard(wizard_model, data_model)


@solara.component
def TabHeader(
    workflow: solara.Reactive[QeDataModel],
    remove_workflow: t.Callable[[int], None],
):
    with solara.Div(class_="tab-header"):
        # TODO stop close event propagation to tab selection (leads to index out of bound)
        solara.IconButton(
            icon_name="mdi-close",
            color="error",
            class_="tab-close-button",
            on_click=remove_workflow,
        )
        solara.v.Icon(
            children=[workflow.value.status_icon],
            class_="status-icon",
        )
        with solara.Div(class_="tab-text"):
            if len(workflow.value.label) > 20:
                with solara.Tooltip(workflow.value.label):
                    solara.Text(workflow.value.label)
            else:
                solara.Text(workflow.value.label)
        if workflow.value.pk:
            solara.Text(f"[{workflow.value.pk}]")


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

    with solara.Div(class_="controls"):
        solara.IconButton(
            color="secondary",
            icon_name="mdi-plus-thick",
            on_click=add_workflow,
        )
        solara.IconButton(
            color="secondary",
            icon_name="mdi-key-plus",
            on_click=prompt_for_pk,
        )

    solara.lab.ConfirmationDialog(
        active_dialog,
        title="Enter workflow PK",
        ok="Submit",
        on_ok=lambda: on_prompt_submit(),
        on_cancel=lambda: set_active_dialog(False),
        children=[
            solara.v.Row(
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
