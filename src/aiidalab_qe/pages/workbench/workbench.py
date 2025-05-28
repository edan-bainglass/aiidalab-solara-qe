from __future__ import annotations

import typing as t

import solara
import solara.lab
import solara.toestand

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

                def remove_this_workflow(index: int = i):
                    remove_workflow(index)

                with solara.lab.Tab(
                    tab_children=[
                        TabHeader(data_model, remove_this_workflow),
                    ],
                ):
                    with solara.Div(class_="workbench-body container"):
                        QeWizard(wizard_model, data_model)


@solara.component
def TabHeader(
    data_model: solara.Reactive[QeDataModel],
    remove_workflow: t.Callable[[int], None],
):
    pk = solara.toestand.Ref(data_model.fields.pk)
    label = solara.toestand.Ref(data_model.fields.label)
    status_icon = solara.toestand.Ref(data_model.fields.status_icon)

    with solara.Div(class_="tab-header"):
        # TODO stop close event propagation to tab selection (leads to index out of bound)
        solara.IconButton(
            icon_name="mdi-close",
            color="error",
            class_="tab-close-button",
            on_click=solara.use_memo(lambda: remove_workflow, []),
        )
        solara.v.Icon(
            children=[status_icon.value],
            class_="status-icon",
        )
        with solara.Div(class_="tab-text"):
            if len(label.value) > 20:
                with solara.Tooltip(label.value):
                    solara.Text(label.value)
            else:
                solara.Text(label.value)
        if pk.value:
            solara.Text(f"[{pk.value}]")


@solara.component
def WorkbenchControls(add_workflow: t.Callable[[int | None], None]):
    input_pk = solara.use_reactive(t.cast(int, None))
    active_dialog = solara.use_reactive(False)

    def prompt_for_pk():
        active_dialog.set(True)

    def submit_dialog():
        add_workflow(input_pk.value)
        input_pk.set(0)
        active_dialog.set(False)

    def close_dialog():
        active_dialog.set(False)
        input_pk.set(0)

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
        active_dialog.value,
        title="Enter workflow PK",
        ok="Submit",
        on_ok=submit_dialog,
        on_cancel=close_dialog,
        children=[
            solara.v.Row(
                children=[
                    solara.InputInt(
                        label="PK",
                        value=input_pk,
                        autofocus=True,
                    ),
                ],
            )
        ],
    )
