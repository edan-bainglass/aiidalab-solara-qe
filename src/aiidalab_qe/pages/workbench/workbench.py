from __future__ import annotations

import typing as t

import solara
import solara.lab
import solara.toestand

from aiidalab_qe.components.wizard import QeWizard
from aiidalab_qe.components.wizard.models import QeWizardModel
from aiidalab_qe.components.wizard.store import WizardStore
from aiidalab_qe.config.paths import STYLES

wizard_store = WizardStore()


@solara.component
def Workbench(store: WizardStore = wizard_store):
    print("\nrendering workbench page")

    def add_workflow(pk: int | None = None):
        store.add_wizard(pk)

    def remove_workflow(uid: str):
        store.remove_wizard(uid)

    wizard_entries = solara.use_memo(
        lambda: list(store.wizards.value.items()),
        [store.wizards.value],
    )

    with solara.Head():
        solara.Style(STYLES / "workbench.css")

    with solara.Div(class_="workbench"):
        WorkbenchControls(add_workflow=add_workflow)
        with solara.lab.Tabs(
            vertical=True,
            lazy=False,
            value=store.active,
        ):
            for uid, wizard_model in wizard_entries:

                def remove_this_workflow(this_uid: str = uid):
                    remove_workflow(this_uid)

                with solara.lab.Tab(
                    tab_children=[
                        TabHeader(
                            wizard_model,
                            remove_this_workflow,
                        ),
                    ],
                ):
                    with solara.Div(class_="workbench-body container"):
                        QeWizard(wizard_model).key(uid)


@solara.component
def TabHeader(
    model: solara.Reactive[QeWizardModel],
    remove_workflow: t.Callable[[int], None],
):
    pk = solara.toestand.Ref(model.fields.pk)
    label = solara.toestand.Ref(model.fields.label)
    status_icon = solara.toestand.Ref(model.fields.status_icon)

    with solara.Div(class_="tab-header"):
        # TODO stop close event propagation to tab selection (leads to index out of bound)
        solara.IconButton(
            icon_name="mdi-close",
            color="error",
            class_="tab-close-button",
            on_click=remove_workflow,
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

    render_context = solara.reacton.core.get_render_context()

    def prompt_for_pk():
        active_dialog.set(True)

    def submit_dialog():
        with render_context:
            add_workflow(input_pk.value)
            input_pk.set(0)
            active_dialog.set(False)

    def close_dialog():
        with render_context:
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
