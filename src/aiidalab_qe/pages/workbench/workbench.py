from __future__ import annotations

import typing as t

import solara
import solara.lab
from solara.toestand import Ref

from aiidalab_qe.components.wizard import QeWizard
from aiidalab_qe.components.wizard.models import QeWizardModel
from aiidalab_qe.components.wizard.store import WizardStore
from aiidalab_qe.config.paths import STYLES

wizard_store = WizardStore()


@solara.component
def Workbench(store: WizardStore = wizard_store):
    print("\nrendering workbench page")

    with solara.Head():
        solara.Style(STYLES / "workbench.css")

    with solara.Div(class_="workbench"):
        WorkbenchControls(store)
        with solara.lab.Tabs(
            vertical=True,
            lazy=False,
            value=store.active,
        ):
            for i, model in enumerate(store.wizards.value):
                with solara.lab.Tab(
                    tab_children=[TabHeader(i, store, model)],
                ):
                    # NOTE: key prevents unnecessary rendering but breaks reactiveness
                    # see https://github.com/widgetti/solara/issues/1060
                    TabBody(model)  # .key(wizard_model.value.uid)


@solara.component
def WorkbenchControls(store: WizardStore):
    input_pk = solara.use_reactive(t.cast(int, None))
    active_dialog = solara.use_reactive(False)

    render_context = solara.reacton.core.get_render_context()

    def prompt_for_pk():
        active_dialog.set(True)

    def submit_dialog():
        with render_context:
            store.add_wizard(input_pk.value)
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
            on_click=store.add_wizard,
        )
        solara.IconButton(
            color="secondary",
            icon_name="mdi-content-copy",
            on_click=store.duplicate_wizard,
            disabled=store.active.value is None,
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


@solara.component
def TabHeader(
    index: int,
    store: WizardStore,
    model: solara.Reactive[QeWizardModel],
):
    pk = Ref(model.fields.pk)
    label = Ref(model.fields.data.label)
    status_icon = Ref(model.fields.status_icon)

    def remove_wizard():
        store.remove_wizard(index)

    with solara.Div(class_="tab-header"):
        # TODO stop close event propagation to tab selection (leads to index out of bound)
        solara.IconButton(
            icon_name="mdi-close",
            color="error",
            class_="tab-close-button",
            on_click=remove_wizard,
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
def TabBody(model: solara.Reactive[QeWizardModel]):
    with solara.Div(class_="workbench-body container"):
        QeWizard(model)
