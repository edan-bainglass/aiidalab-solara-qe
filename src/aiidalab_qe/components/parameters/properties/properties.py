from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.plugins.utils import get_plugin_titles

PROPERTY_TITLES = get_plugin_titles()


@solara.component
def PropertiesSelector(model: solara.Reactive[QeAppModel]):
    properties = Ref(model.fields.properties)

    with solara.Div(class_="properties-selector"):
        print("\nrendering properties-selector component")

        for prop, title in PROPERTY_TITLES.items():

            def update_properties(checked: bool, prop: str = prop):
                properties.set(
                    [*properties.value, prop]
                    if checked
                    else [*filter(lambda p: p != prop, properties.value)]
                )

            solara.Checkbox(
                label=title,
                value=prop in properties.value,
                on_value=update_properties,
            )
