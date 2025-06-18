import typing as t

from pymatgen.core import Element


def get_manifold(element: Element) -> t.Optional[str]:
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
