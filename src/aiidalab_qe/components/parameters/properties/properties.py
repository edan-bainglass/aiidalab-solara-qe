from __future__ import annotations

import solara

from aiidalab_qe.plugins.utils import get_plugin_titles

PROPERTY_TITLES = get_plugin_titles()


@solara.component
def PropertiesSelector(properties: solara.Reactive[list[str]]):
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
