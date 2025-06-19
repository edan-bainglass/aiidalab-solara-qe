from __future__ import annotations

import typing as t

import solara
from aiida_pseudo.common.units import U
from aiida_pseudo.data.pseudo import PseudoPotentialData
from solara.toestand import Ref

from aiidalab_qe.common.components.selection import ToggleButtons
from aiidalab_qe.common.models.schema import QeAppModel
from aiidalab_qe.common.services.aiida import AiiDAService

from .uploader import PseudoUploadComponent

SSSP_VERSION = "1.3"
PSEUDODOJO_VERSION = "0.4"


@solara.component
def PseudopotentialsSettings(active: bool, model: solara.Reactive[QeAppModel]):
    process = Ref(model.fields.process)
    input_structure = Ref(model.fields.input_structure)
    parameters = model.fields.calculation_parameters
    protocol = Ref(parameters.basic.protocol)
    spin_orbit = Ref(parameters.basic.spin_orbit)
    pseudos = Ref(parameters.advanced.pw.pseudos)
    pseudo_family = Ref(parameters.advanced.pseudo_family)
    ecutwfc = Ref(parameters.advanced.pw.parameters.SYSTEM.ecutwfc)
    ecutrho = Ref(parameters.advanced.pw.parameters.SYSTEM.ecutrho)
    functional = solara.use_reactive("PBEsol")

    disabled = solara.use_memo(
        lambda: process.value is not None,
        [process.value],
    )

    library_options = solara.use_memo(
        lambda: (
            ("PseudoDojo",)
            if spin_orbit.value == "soc"
            else (
                "SSSP",
                "PseudoDojo",
            )
        ),
        [spin_orbit.value],
    )

    library = solara.use_reactive(library_options[0])

    accuracy_options = solara.use_memo(
        lambda: (
            {
                "efficiency": {
                    "label": "Efficiency",
                },
                "precision": {
                    "label": "Precision",
                },
            }
            if library.value == "SSSP"
            else {
                "standard": {
                    "label": "Standard",
                },
                "stringent": {
                    "label": "Stringent",
                },
            }
            if library.value == "PseudoDojo"
            else []
        ),
        [library.value],
    )

    def get_default_accuracy() -> str:
        if library.value == "SSSP":
            return "precision" if protocol.value == "stringent" else "efficiency"
        elif library.value == "PseudoDojo":
            return "stringent" if protocol.value == "stringent" else "standard"
        else:
            return ""

    default_accuracy = solara.use_memo(
        get_default_accuracy,
        [library.value, protocol.value],
    )

    accuracy = solara.use_reactive(default_accuracy)

    def get_family_link() -> str:
        if library.value == "SSSP":
            pseudo_family_link = (
                f"https://www.materialscloud.org/discover/sssp/table/{accuracy.value}"
            )
        else:
            pseudo_family_link = "http://www.pseudo-dojo.org/"

        return pseudo_family_link

    family_link = solara.use_memo(
        get_family_link,
        [library.value, accuracy.value],
    )

    # Caches to avoid DB re-fetching and/or re-computation
    pseudo_filenames = solara.use_reactive(t.cast(dict[str, str], {}))
    pseudo_cutoffs = solara.use_reactive(([0.0], [0.0]))

    ready = input_structure.value and all(
        [
            all(
                [
                    kind_name in container
                    for container in (
                        pseudos.value,
                        pseudo_filenames.value,
                    )
                ]
            )
            for kind_name in input_structure.value.get_kind_names()
        ]
    )

    def set_pseudo_family():
        lib = library.value
        fun = functional.value
        acc = accuracy.value
        if lib == "PseudoDojo":
            ver = PSEUDODOJO_VERSION
            rel = "FR" if spin_orbit.value == "soc" else "SR"
            family_string = f"{lib}/{ver}/{fun}/{rel}/{acc}/upf"
        elif lib == "SSSP":
            ver = SSSP_VERSION
            family_string = f"{lib}/{ver}/{fun}/{acc}"
        else:
            print(f"Unknown pseudo family parameters: {lib} | {fun} | {acc}")
            family_string = ""
        pseudo_family.set(family_string)

    def set_defaults():
        if not (
            input_structure.value
            and (family := AiiDAService.load_pseudo_family(pseudo_family.value))
        ):
            return

        default_pseudos = t.cast(
            dict[str, PseudoPotentialData],
            family.get_pseudos(structure=input_structure.value),
        )

        current_unit = family.get_cutoffs_unit()
        cutoffs = family.get_cutoffs()

        new_pseudos = {}
        new_filenames = {}
        new_cutoffs = [[], []]

        for kind in input_structure.value.kinds:
            pseudo = default_pseudos.get(kind.name)
            new_pseudos[kind.name] = pseudo.uuid
            new_filenames[kind.name] = AiiDAService.get_pseudo(pseudo.uuid).filename
            kind_cutoffs: dict = cutoffs.get(kind.symbol, {})
            kind_cutoffs_Ry = {
                key: U.Quantity(v, current_unit).to("Ry").to_tuple()[0]
                for key, v in kind_cutoffs.items()
            }
            new_cutoffs[0].append(kind_cutoffs_Ry.get("cutoff_wfc", 0.0))
            new_cutoffs[1].append(kind_cutoffs_Ry.get("cutoff_rho", 0.0))

        pseudos.set(new_pseudos)
        ecutwfc.set(max(new_cutoffs[0]))
        ecutrho.set(max(new_cutoffs[1]))
        pseudo_filenames.set(new_filenames)
        pseudo_cutoffs.set(new_cutoffs)

    def update_panel():
        if input_structure.value:
            set_defaults()

    solara.use_effect(
        set_pseudo_family,
        [functional.value, library.value, accuracy.value],
    )

    solara.use_effect(
        update_panel,
        [input_structure.value, pseudo_family.value],
    )

    with solara.Div(
        class_=" ".join(
            [
                "control-group pseudos-settings",
                *(["d-none"] if not active else []),
            ],
        ),
    ):
        if not (active and ready):
            return

        print("\nrendering pseudos-settings component")

        ToggleButtons(
            label="Functional",
            options=(
                "PBE",
                "PBEsol",
            ),
            value=functional,
        )
        ToggleButtons(
            label="Library",
            options=library_options,
            value=library,
        )
        ToggleButtons(
            label="Accuracy",
            options=accuracy_options,
            value=accuracy,
        )

        with solara.Row(classes=["pseudo-cutoffs"]):
            solara.Text(
                "Cutoffs (Ry)",
                classes=["cutoffs-label"],
            )
            solara.InputText(
                label="ψ",
                value=ecutwfc,
                classes=["cutoff-input"],
            )
            solara.InputText(
                label="ρ",
                value=ecutrho,
                classes=["cutoff-input"],
            )

        with solara.Div(class_="pseudos-list"):
            for i, kind in enumerate(input_structure.value.kinds):

                def update(value: str, filename: str):
                    new_pseudos = pseudos.value.copy()
                    new_pseudo_filenames = pseudo_filenames.value.copy()
                    new_pseudos[kind.name] = value
                    new_pseudo_filenames[kind.name] = filename
                    pseudos.set(new_pseudos)
                    pseudo_filenames.set(new_pseudo_filenames)

                PseudoUploadComponent(
                    kind_name=kind.name,
                    pseudo_filename=pseudo_filenames.value.get(kind.name),
                    cutoffs=(pseudo_cutoffs.value[0][i], pseudo_cutoffs.value[1][i]),
                    update=update,
                )

        with solara.Div(class_="pseudo-family-link"):
            solara.HTML(
                "span",
                f"Click <a href='{family_link}' target='_blank'>here</a> for more information about the selected pseudopotential family",
            )
