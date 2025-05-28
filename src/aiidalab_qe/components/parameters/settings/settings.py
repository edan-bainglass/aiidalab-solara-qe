from __future__ import annotations

import solara
import solara.toestand

from aiidalab_qe.components.wizard.models import QeDataModel
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
def CalculationSettings(data_model: solara.Reactive[QeDataModel]):
    calculation_parameters = solara.toestand.Ref(
        data_model.fields.data.calculation_parameters
    )
    category = solara.use_reactive("basic")

    with solara.Div(class_="calculation-settings"):
        solara.Select(
            label="Category",
            values=[
                category
                for category in CATEGORIES
                if category
                in {
                    *calculation_parameters.value.properties,
                    *BUILTIN_CATEGORIES,
                }
            ],
            value=category,
            classes=["category-selector"],
        )
        CATEGORIES[category.value](data_model)
