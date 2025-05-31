from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.components.wizard.models import QeWizardModel
from aiidalab_qe.plugins.utils import get_plugin_titles

PROPERTY_TITLES = get_plugin_titles()


@solara.component
def PropertiesSelector(model: solara.Reactive[QeWizardModel]):
    properties = Ref(model.fields.data.calculation_parameters.properties)

    def update_properties(prop: str, checked: bool):
        properties.set(
            [*properties.value, prop]
            if checked
            else [*filter(lambda p: p != prop, properties.value)]
        )

    with solara.Div(class_="properties-selector"):
        for prop, title in PROPERTY_TITLES.items():
            solara.Checkbox(
                label=title,
                value=prop in properties.value,
                on_value=lambda checked, prop=prop: update_properties(prop, checked),
            )
