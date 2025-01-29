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

    with solara.v.Row():
        with solara.v.Col(md=6, lg=4, xl=3):
            solara.Select(
                label="Category",
                values=[*CATEGORIES.keys()],
                value=category,
            )

    CATEGORIES[category.value](data_model)
