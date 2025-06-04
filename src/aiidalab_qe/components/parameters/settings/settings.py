from __future__ import annotations

import solara
import solara.toestand

from aiidalab_qe.components.wizard.models import QeWizardModel
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
def CalculationSettings(model: solara.Reactive[QeWizardModel]):
    properties = solara.toestand.Ref(model.fields.data.properties)
    category = solara.use_reactive("basic")

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
                    value=category,
                )
        CATEGORIES[category.value](model)
