from __future__ import annotations

import typing as t

import solara
from solara.toestand import Ref

from aiidalab_qe.components.wizard.models import QeDataModel

MOLECULAR_RELAXATION_OPTIONS = {
    "positions": {
        "label": "Atomic positions",
        "icon": "mdi-grain",
        "description": "Optimize atomic positions only",
    },
}

STRUCTURAL_RELAXATION_OPTIONS = {
    **MOLECULAR_RELAXATION_OPTIONS,
    "positions_cell": {
        "label": "Full geometry",
        "icon": "mdi-cube",
        "description": "Optimize atomic positions and cell geometry",
    },
}


@solara.component
def RelaxationSelector(data_model: solara.Reactive[QeDataModel]):
    input_structure = Ref(data_model.fields.data.input_structure)
    relax_type = Ref(data_model.fields.data.calculation_parameters.relax_type)
    is_relax = solara.use_reactive(relax_type.value not in (None, "none"))
    options = solara.use_reactive(t.cast(list[str], []))

    OPTIONS = (
        STRUCTURAL_RELAXATION_OPTIONS
        if input_structure.value and any(input_structure.value.pbc)
        else MOLECULAR_RELAXATION_OPTIONS
    )

    def set_relaxation_options():
        old_relax_type = relax_type.value
        options.set([*OPTIONS.keys()])
        relax_type.set(old_relax_type)

    def set_default_relax_type():
        type_ = data_model.value.data.calculation_parameters.model_fields["relax_type"]
        relax_type.set(type_.default if is_relax.value else "none")

    def update_relaxation(type_: str):
        is_relax.set(type_ != "none")
        relax_type.set(type_)

    solara.use_effect(
        set_relaxation_options,
        [input_structure.value],
    )

    solara.use_effect(
        set_default_relax_type,
        [is_relax.value],
    )

    with solara.v.Container(class_="relaxation-selector"):
        solara.Switch(
            label="Relax structure",
            value=is_relax,
        )
        if is_relax.value and options.value:
            with solara.ToggleButtonsSingle(
                value=relax_type.value,
                on_value=update_relaxation,
                dense=True,
            ):
                for option in options.value:
                    solara.Button(
                        label=OPTIONS[option]["label"],
                        icon_name=OPTIONS[option]["icon"],
                        tooltip=OPTIONS[option]["description"],  # TODO get this to work
                        value=option,
                    )
