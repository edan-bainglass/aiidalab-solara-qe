from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.common.components.wizard import WizardState, onStateChange
from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.config.paths import STYLES
from aiidalab_qe.plugins.utils import get_plugin_settings

from .advanced import AdvancedSettings
from .basic import BasicSettings

plugin_entries = {
    plugin: settings.component
    for (
        plugin,
        settings,
    ) in get_plugin_settings().items()
}

BUILTIN_CATEGORIES = {
    "basic": BasicSettings,
    "advanced": AdvancedSettings,
}

CATEGORIES = {
    **BUILTIN_CATEGORIES,
    **plugin_entries,
}


@solara.component
def ParametersConfigurationStep(
    model: solara.Reactive[QeAppModel],
    on_state_change: onStateChange,
):
    process = Ref(model.fields.process)
    parameters = Ref(model.fields.calculation_parameters)
    properties = Ref(model.fields.properties)
    active_panel = solara.use_reactive("basic")

    disabled = solara.use_memo(
        lambda: process.value is not None,
        [process.value],
    )

    active_categories = solara.use_memo(
        lambda: [
            category.capitalize()
            for category in CATEGORIES
            if category
            in {
                *BUILTIN_CATEGORIES,
                *properties.value,
            }
        ],
        [properties.value],
    )

    def redirect_to_valid_panel():
        if active_panel.value not in active_categories:
            active_panel.set("basic")

    def update_state():
        if disabled:
            return

        if not parameters.value:
            new_state = WizardState.READY
        else:
            new_state = WizardState.CONFIGURED

        on_state_change(new_state)

    solara.use_effect(
        redirect_to_valid_panel,
        [properties.value],
    )

    solara.use_effect(
        update_state,
        [parameters.value],
    )

    with solara.Head():
        solara.Style(STYLES / "parameters.css")

    with solara.Div(class_="parameters-configuration-step"):
        print("\nrendering parameters-configuration-step component")

        solara.Select(
            label="",
            values=active_categories,
            value=active_panel.value.capitalize(),
            on_value=lambda v: active_panel.set(v.lower()),
            classes=["parameters-category-selector"],
        )

        for panel_key, SettingsPanel in CATEGORIES.items():
            if panel_key in BUILTIN_CATEGORIES or panel_key in properties.value:
                SettingsPanel(
                    active=active_panel.value == panel_key,
                    model=model,
                )
