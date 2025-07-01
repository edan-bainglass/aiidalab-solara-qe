from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.plugins.utils import get_plugin_titles

PROPERTY_TITLES = get_plugin_titles()


@solara.component
def PropertiesSelector(model: solara.Reactive[QeAppModel]):
    process = Ref(model.fields.process)
    properties = Ref(model.fields.properties)

    disabled = solara.use_memo(
        lambda: process.value is not None,
        [process.value],
    )

    with solara.Div(class_="properties-selector"):
        print("rendering properties-selector component")

        for prop, title in PROPERTY_TITLES.items():

            def update_properties(checked: bool, prop: str = prop):
                properties.set(
                    [*properties.value, prop]
                    if checked
                    else [*filter(lambda p: p != prop, properties.value)]
                )

            # TODO triggers multiple re-renders - investigate!
            solara.Checkbox(
                label=title,
                value=prop in properties.value,
                on_value=update_properties,
                disabled=disabled,
            )
