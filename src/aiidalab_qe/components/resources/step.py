from __future__ import annotations

import solara
import solara.toestand

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.common.models.codes import ResourcesModel
from aiidalab_qe.components.resources.resource import ResourceCard
from aiidalab_qe.components.wizard.models import QeWizardModel
from aiidalab_qe.config.paths import STYLES
from aiidalab_qe.plugins.models import PluginResourcesModel
from aiidalab_qe.plugins.utils import get_plugin_resources

plugin_entries = {
    plugin: resources.codes
    for (
        plugin,
        resources,
    ) in get_plugin_resources().items()
}

BUILTIN_CATEGORIES = {
    "global": "",
}

CATEGORIES = {
    **BUILTIN_CATEGORIES,
    **plugin_entries,
}


@solara.component
def ResourcesSelectionStep(
    model: solara.Reactive[QeWizardModel],
    on_state_change: onStateChange,
):
    print("\nrendering computational-resources-step component")

    resources = solara.toestand.Ref(model.fields.data.computational_resources)
    process = solara.toestand.Ref(model.fields.data.process)
    category = solara.use_reactive("global")

    def update_state():
        if not resources.value:
            new_state = WizardState.READY
        elif process.value:
            new_state = WizardState.SUCCESS
        else:
            new_state = WizardState.CONFIGURED

        on_state_change(new_state)

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
                    values=list(CATEGORIES.keys()),
                    value=category,
                )

        global_resources = solara.toestand.Ref(resources.fields.global_)

        if category.value == "global":
            ResourcesPanel(global_resources)
        else:
            plugin_fields = resources.fields.plugins[category.value]
            plugin_resources = solara.toestand.Ref(plugin_fields)
            PluginResourcesPanel(plugin_resources, global_resources)


@solara.component
def ResourcesPanel(model: solara.Reactive[ResourcesModel]):
    with solara.Div(class_="row g-0 row-gap-3 column-gap-3"):
        for code_key in model.value.codes:
            code_model = solara.toestand.Ref(model.fields.codes[code_key])
            ResourceCard(
                code_model,
                label=f"{code_model.value.name} ({code_key})",
            )


@solara.component
def PluginResourcesPanel(
    model: solara.Reactive[PluginResourcesModel],
    global_model: solara.Reactive[ResourcesModel],
):
    override = solara.toestand.Ref(model.fields.override)

    def on_override_toggle():
        override.set(not override.value)
        if not override.value:
            model.set(
                model.value.model_copy(
                    update={
                        "codes": {
                            **model.value.codes.copy(),
                            **global_model.value.codes.copy(),
                        },
                    }
                )
            )

    solara.Checkbox(
        style="margin-bottom: 1rem;",
        label="Override global resources",
        value=override.value,
        on_value=lambda _: on_override_toggle(),
    )
    if override.value:
        ResourcesPanel(model)
