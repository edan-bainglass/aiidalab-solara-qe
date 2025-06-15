from __future__ import annotations

import solara
from aiida import orm

from aiidalab_qe.common.models.schema import CalculationParametersModel
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
def CalculationSettings(
    properties: solara.Reactive[list[str]],
    input_structure: solara.Reactive[orm.StructureData],
    parameters: solara.Reactive[CalculationParametersModel],
):
    active_panel = solara.use_reactive("basic")

    with solara.Div(class_="calculation-settings"):
        with solara.Row(classes=["mb-2"]):
            with solara.Column():
                solara.Select(
                    label="Category",
                    values=[
                        category
                        for category in CATEGORIES
                        if category
                        in {
                            *properties.value,
                            *BUILTIN_CATEGORIES,
                        }
                    ],
                    value=active_panel,
                )

        for panel_key, SettingsPanel in CATEGORIES.items():
            if panel_key in BUILTIN_CATEGORIES or panel_key in properties.value:
                SettingsPanel(
                    active=active_panel.value == panel_key,
                    input_structure=input_structure,
                    parameters=parameters,
                )
