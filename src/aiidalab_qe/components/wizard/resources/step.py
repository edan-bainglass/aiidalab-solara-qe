from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.common.models.codes import CodeModel
from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.config.paths import STYLES
from aiidalab_qe.plugins.models import PluginResourcesModel

from .resource import ResourceCard


@solara.component
def ResourcesSelectionStep(
    model: solara.Reactive[QeAppModel],
    on_state_change: onStateChange,
):
    process = Ref(model.fields.process)
    properties = Ref(model.fields.properties)
    resources = Ref(model.fields.computational_resources)
    active = Ref(resources.fields.active)
    global_codes = Ref(resources.fields.global_.codes)

    disabled = solara.use_memo(
        lambda: process.value is not None,
        [process.value],
    )

    def update_state():
        if disabled:
            return

        if not resources.value:
            new_state = WizardState.READY
        else:
            new_state = WizardState.CONFIGURED

        on_state_change(new_state)

    def set_global_codes():
        # TODO possible optimization; consider building once and toggling (in)active

        plugin_resources = resources.value.plugins
        plugin_mapping = resources.value.plugin_mapping
        pw_code = resources.value.global_.codes["pw"]
        codes = {
            "pw": pw_code,
        }

        for prop in properties.value:
            if prop == "relax" or prop not in plugin_resources:
                continue

            plugin_codes = plugin_resources[prop].codes
            for code_key, code_model in plugin_codes.items():
                if (global_key := plugin_mapping[code_key]) not in codes:
                    codes[global_key] = code_model.model_copy()

        global_codes.set(codes)
        active.set("global")

    solara.use_effect(
        update_state,
        [resources.value],
    )

    solara.use_effect(
        set_global_codes,
        [properties.value],
    )

    with solara.Head():
        solara.Style(STYLES / "resources.css")

    with solara.Div(class_="resources-selection-step"):
        print("rendering computational-resources-step component")

        with solara.Row(classes=["mb-2"]):
            with solara.Column():
                solara.Select(
                    label="Category",
                    values=["global", *[p for p in properties.value if p != "relax"]],
                    value=active,
                )

        ResourcesPanel(
            active=active.value == "global",
            codes=global_codes,
            disabled=disabled,
        )
        for prop in properties.value:
            PluginResourcesPanel(
                active=active.value == prop,
                model=Ref(resources.fields.plugins[prop]),
                global_codes=global_codes,
                disabled=disabled,
            )


@solara.component
def ResourcesPanel(
    active: bool,
    codes: solara.Reactive[dict[str, CodeModel]],
    disabled: bool = False,
):
    with solara.v.Row(
        class_=" ".join(
            [
                "resources-panel",
                *(["d-none"] if not active else []),
            ],
        ),
    ):
        for code_key in codes.value:
            code_model = Ref(codes.fields[code_key])
            ResourceCard(code_model, disabled=disabled)


@solara.component
def PluginResourcesPanel(
    active: bool,
    model: solara.Reactive[PluginResourcesModel],
    global_codes: solara.Reactive[dict[str, CodeModel]],
    disabled: bool = False,
):
    plugin_codes = Ref(model.fields.codes)
    override = Ref(model.fields.override)

    def reset_codes_to_global():
        global_plugin_codes = {
            code_key: code_model.model_copy()
            for code_key, code_model in global_codes.value.items()
            if code_key in plugin_codes.value
        }
        model.set(
            model.value.model_copy(
                update={
                    "codes": {
                        **plugin_codes.value,
                        **global_plugin_codes,
                    },
                }
            )
        )

    def on_override_toggle(value: bool):
        reset_codes_to_global()
        override.set(value)

    with solara.Div(
        class_=" ".join(
            [
                "resources-panel",
                *(["d-none"] if not active else []),
            ],
        ),
    ):
        solara.Checkbox(
            style="margin-bottom: 1rem;",
            label="Override global resources",
            value=override.value,
            on_value=on_override_toggle,
            disabled=disabled,
        )
        if override.value:
            ResourcesPanel(
                active=active,
                codes=plugin_codes,
                disabled=disabled,
            )
