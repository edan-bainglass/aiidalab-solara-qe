from __future__ import annotations

import solara
from aiida_quantumespresso.data.hubbard_structure import (
    HubbardParameters,
    HubbardStructureData,
)
from pymatgen.core import Element
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import QeAppModel

from .eigenvalues_input import EigenvaluesInput
from .u_param_input import HubbardUParameterInput
from .utils import get_manifold


@solara.component
def HubbardUSettings(active: bool, model: solara.Reactive[QeAppModel]):
    input_structure = Ref(model.fields.input_structure)
    hubbard_settings = model.fields.calculation_parameters.advanced.hubbard_parameters
    use_hubbard_u = Ref(hubbard_settings.use_hubbard_u)
    use_eigenvalues = Ref(hubbard_settings.use_eigenvalues)
    hubbard_u = Ref(hubbard_settings.hubbard_u)
    eigenvalues = Ref(hubbard_settings.eigenvalues)

    def get_orbital_labels() -> list[str]:
        return (
            [
                f"{kind_name} - {manifold}"
                for kind_name, manifold in zip(
                    input_structure.value.get_kind_names(),
                    [
                        get_manifold(Element(kind.symbol))
                        for kind in input_structure.value.kinds
                    ],
                )
            ]
            if input_structure.value
            else []
        )

    def get_valid_kinds() -> list[tuple[str, int]]:
        if not input_structure.value:
            return []

        valid: list[tuple[str, int]] = []
        for kind in input_structure.value.kinds:
            element = Element(kind.symbol)
            if (
                element.is_transition_metal
                or element.is_lanthanoid
                or element.is_actinoid
            ):
                num_states = 5 if element.is_transition_metal else 7
                valid.append((kind.name, num_states))

        return valid

    orbital_labels = solara.use_memo(
        get_orbital_labels,
        [input_structure.value],
    )

    valid_kinds = solara.use_memo(
        get_valid_kinds,
        [input_structure.value],
    )

    def set_parameters_from_hubbard_structure():
        hubbard_structure: HubbardStructureData = input_structure.value  # type: ignore
        hubbard_parameters: list[HubbardParameters] = (
            hubbard_structure.hubbard.model_dump().get("parameters", [])
        )
        sites = hubbard_structure.sites
        hubbard_u.set(
            {
                f"{sites[hp.atom_index].kind_name} - {hp.atom_manifold}": hp.value
                for hp in hubbard_parameters
            }
        )
        use_hubbard_u.set(True)

    def reset_hubbard_u():
        hubbard_u.set({label: 0.0 for label in orbital_labels})

    def reset_eigenvalues():
        eigenvalues.set(
            [
                [
                    [
                        [state + 1, spin, kind_name, -1.0]  # eigenvalue
                        for state in range(num_states)
                    ]
                    for spin in [1, 2]  # spin up and down
                ]
                for kind_name, num_states in valid_kinds
            ]
        )

    def reset_hubbard_parameters():
        use_hubbard_u.set(False)
        use_eigenvalues.set(False)
        if isinstance(input_structure.value, HubbardStructureData):
            set_parameters_from_hubbard_structure()
        else:
            reset_hubbard_u()
        reset_eigenvalues()

    solara.use_effect(
        reset_hubbard_parameters,
        [input_structure.value],
    )

    with solara.Div(
        class_=" ".join(
            [
                "control-group hubbard-settings",
                *(["d-none"] if not active else []),
            ],
        ),
    ):
        if not active:
            return

        print("\nrendering hubbard-settings component")

        solara.Checkbox(
            label="Use Hubbard U",
            value=use_hubbard_u,
        )

        if use_hubbard_u.value:
            for label in orbital_labels:
                HubbardUParameterInput(
                    label=label,
                    u_parameter=hubbard_u.value.get(label, 0.0),
                    on_change=lambda u, label=label: hubbard_u.set(
                        {
                            **hubbard_u.value,
                            label: u,
                        }
                    ),
                )

            if valid_kinds:
                solara.Checkbox(
                    label="Define eigenvalues",
                    value=use_eigenvalues,
                )

                if use_eigenvalues.value:
                    for i, (kind_name, num_states) in enumerate(valid_kinds):
                        EigenvaluesInput(
                            kind_index=i,
                            kind_name=kind_name,
                            num_states=num_states,
                            eigenvalues=eigenvalues,
                        )
