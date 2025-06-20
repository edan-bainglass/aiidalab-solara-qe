from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import QeAppModel
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
def CalculationSettings(model: solara.Reactive[QeAppModel]):
    properties = Ref(model.fields.properties)
    active_panel = solara.use_reactive("basic")

    with solara.Div(class_="calculation-settings"):
        solara.Select(
            label="",
            values=[
                category.capitalize()
                for category in CATEGORIES
                if category
                in {
                    *BUILTIN_CATEGORIES,
                    *properties.value,
                }
            ],
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
