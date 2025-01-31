from __future__ import annotations

import solara

from aiidalab_qe.components.wizard.models import QeDataModel

from .advanced import AdvancedSettings
from .basic import BasicSettings


CATEGORIES = {
    "basic": BasicSettings,
    "advanced": AdvancedSettings,
}


@solara.component
def CalculationSettings(data_model: solara.Reactive[QeDataModel]):
    category = solara.use_reactive("basic")

    with solara.Div(class_="calculation-settings"):
        solara.Select(
            label="Category",
            values=[*CATEGORIES.keys()],
            value=category,
            classes=["category-selector"],
        )
        CATEGORIES[category.value](data_model)
