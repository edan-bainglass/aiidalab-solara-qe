from __future__ import annotations

import typing as t

import solara
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import QeAppModel

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
def RelaxationSelector(model: solara.Reactive[QeAppModel]):
    # TODO check if effects are optimal (options may not need to be reactive)
    process = Ref(model.fields.process)
    input_structure = Ref(model.fields.input_structure)
    relax_type = Ref(model.fields.calculation_parameters.relax_type)
    is_relax = solara.use_reactive(relax_type.value not in (None, "none"))
    options = solara.use_reactive(t.cast(dict[str, dict[str, str]], {}))

    disabled = solara.use_memo(
        lambda: process.value is not None,
        [process.value],
    )

    def set_relaxation_options():
        options.set(
            STRUCTURAL_RELAXATION_OPTIONS
            if input_structure.value and any(input_structure.value.pbc)
            else MOLECULAR_RELAXATION_OPTIONS
        )
        relax_type.set([*options.value.keys()][-1])

    def set_default_relax_type():
        relax_type.set([*options.value.keys()][-1] if is_relax.value else "none")

    solara.use_effect(
        set_relaxation_options,
        [input_structure.value],
    )

    solara.use_effect(
        set_default_relax_type,
        [is_relax.value],
    )

    with solara.Div(class_="relaxation-selector"):
        print("\nrendering relaxation-selector component")

        solara.Switch(
            label="Relax structure",
            value=is_relax,
            classes=["relaxation-switch"],
            disabled=disabled,
        )
        if is_relax.value:
            if not options.value:
                with solara.Div(class_="spinner"):
                    solara.SpinnerSolara()
            else:
                with solara.ToggleButtonsSingle(
                    value=relax_type,
                    dense=True,
                ):
                    for option, props in options.value.items():
                        solara.Button(
                            label=props["label"],
                            icon_name=props["icon"],
                            tooltip=props["description"],
                            value=option,
                            disabled=disabled,
                        )
