from __future__ import annotations

import solara
import solara.toestand

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.common.models.codes import CodeModel
from aiidalab_qe.components.resources.resource import ResourceCard
from aiidalab_qe.components.wizard.models import QeWizardModel
from aiidalab_qe.config.paths import STYLES
from aiidalab_qe.plugins.models import PluginResourcesModel


@solara.component
def ResourcesSelectionStep(
    model: solara.Reactive[QeWizardModel],
    on_state_change: onStateChange,
):
    print("\nrendering computational-resources-step component")

    properties = solara.toestand.Ref(model.fields.data.properties)
    resources = solara.toestand.Ref(model.fields.data.computational_resources)
    process = solara.toestand.Ref(model.fields.data.process)
    active = solara.toestand.Ref(resources.fields.active)

    global_codes = solara.toestand.Ref(resources.fields.global_.codes)

    def update_state():
        if not resources.value:
            new_state = WizardState.READY
        elif process.value:
            new_state = WizardState.SUCCESS
        else:
            new_state = WizardState.CONFIGURED

        on_state_change(new_state)

    def build_global_codes():
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
        build_global_codes,
        [properties.value],
    )

    solara.use_effect(
        update_state,
        [resources.value],
    )

    with solara.Head():
        solara.Style(STYLES / "resources.css")

    with solara.Div(class_="resources-selection-step"):
        with solara.Row(classes=["mb-2"]):
            with solara.Column():
                solara.Select(
                    label="Category",
                    values=["global", *[p for p in properties.value if p != "relax"]],
                    value=active,
                )

        if active.value == "global":
            ResourcesPanel(global_codes)
        else:
            plugin_fields = resources.fields.plugins[active.value]
            this_plugin_resources = solara.toestand.Ref(plugin_fields)
            PluginResourcesPanel(this_plugin_resources, global_codes)


@solara.component
def ResourcesPanel(codes: solara.Reactive[dict[str, CodeModel]]):
    with solara.v.Row(class_="resources-panel"):
        for code_key in codes.value:
            code_model = solara.toestand.Ref(codes.fields[code_key])
            ResourceCard(code_model)


@solara.component
def PluginResourcesPanel(
    model: solara.Reactive[PluginResourcesModel],
    global_codes: solara.Reactive[dict[str, CodeModel]],
):
    plugin_codes = solara.toestand.Ref(model.fields.codes)
    override = solara.toestand.Ref(model.fields.override)

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

    def on_override_toggle():
        reset_codes_to_global()
        override.set(not override.value)

    solara.Checkbox(
        style="margin-bottom: 1rem;",
        label="Override global resources",
        value=override.value,
        on_value=lambda _: on_override_toggle(),
    )
    if override.value:
        ResourcesPanel(plugin_codes)
