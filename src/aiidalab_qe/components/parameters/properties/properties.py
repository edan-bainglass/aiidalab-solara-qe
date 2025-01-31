from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.components.wizard.models import QeDataModel

PROPERTIES_MAP = {
    "bands": {"label": "Electronic band structure"},
    "pdos": {"label": "Electronic projected density of states"},
}


@solara.component
def PropertiesSelector(data_model: solara.Reactive[QeDataModel]):
    properties = Ref(data_model.fields.data.calculation_parameters.properties)

    def update_properties(prop: str, checked: bool):
        properties.set(
            [*properties.value, prop]
            if checked
            else [*filter(lambda p: p != prop, properties.value)]
        )

    with solara.Div(class_="properties-selector"):
        for prop, prop_data in PROPERTIES_MAP.items():
            solara.Checkbox(
                label=prop_data["label"],
                value=prop in properties.value,
                on_value=lambda checked, prop=prop: update_properties(prop, checked),
            )
