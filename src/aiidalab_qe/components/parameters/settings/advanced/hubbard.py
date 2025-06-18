from __future__ import annotations

from copy import deepcopy
import typing as t

import solara
from aiida import orm
from aiida_quantumespresso.data.hubbard_structure import (
    HubbardStructureData,
    HubbardParameters,
)
from pymatgen.core import Element
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import CalculationParametersModel


@solara.component
def HubbardUSettings(
    active: bool,
    input_structure: solara.Reactive[orm.StructureData],
    parameters: solara.Reactive[CalculationParametersModel],
):
    hubbard_settings = parameters.fields.advanced.hubbard_parameters
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
                        _get_manifold(Element(kind.symbol))
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


@solara.component
def HubbardUParameterInput(
    label: str,
    u_parameter: float,
    on_change: t.Callable[[float], None],
):
    return solara.InputFloat(
        label=label,
        value=u_parameter,
        on_value=on_change,
    )


@solara.component
def EigenvaluesInput(
    kind_index: int,
    kind_name: str,
    num_states: int,
    eigenvalues: solara.Reactive[list[list[list[tuple[int, int, str, float]]]]],
):
    kind_eigenvalues = eigenvalues.value[kind_index]
    with solara.Row():
        with solara.Column():
            solara.Text(f"{kind_name}")
        with solara.Column():
            for spin_index, spin_label in enumerate(("Up", "Down")):
                with solara.Row():
                    solara.Text(spin_label)
                    for state_index in range(num_states):

                        def update_eigenvalue(
                            value: str,
                            state: int = state_index,
                            spin: int = spin_index,
                            kind: int = kind_index,
                        ):
                            eigvals = deepcopy(eigenvalues.value)
                            eigvals[kind][spin][state] = (
                                state,
                                spin,
                                kind_name,
                                float(value),
                            )
                            eigenvalues.set(eigvals)

                        eigenvalue = kind_eigenvalues[spin_index][state_index][-1]
                        solara.Select(
                            label=f"{state_index + 1}",
                            values=["-1", "0", "1"],
                            value=str(int(eigenvalue)),
                            on_value=update_eigenvalue,
                        )


def _get_manifold(element: Element) -> t.Optional[str]:
    valence = [
        orbital
        for orbital in element.electronic_structure.split(".")
        if "[" not in orbital
    ]
    orbital_shells = [shell[:2] for shell in valence]

    def is_condition_met(shell):
        return condition and condition in shell

    # Conditions for determining the Hubbard manifold
    # to be selected from the electronic structure
    conditions = {
        element.is_transition_metal: "d",
        element.is_lanthanoid or element.is_actinoid: "f",
        element.is_post_transition_metal
        or element.is_metalloid
        or element.is_halogen
        or element.is_chalcogen
        or element.symbol in ["C", "N", "P"]: "p",
        element.is_alkaline or element.is_alkali or element.is_noble_gas: "s",
        element.symbol in ["H", "He"]: "s",
    }

    condition = next(
        (shell for condition, shell in conditions.items() if condition),
        None,
    )

    hubbard_manifold = next(
        (shell for shell in orbital_shells if is_condition_met(shell)),
        None,
    )

    return hubbard_manifold
