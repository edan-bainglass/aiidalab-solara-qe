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
    pseudo_family = Ref(parameters.advanced.pseudo_family_parameters)
    functional = Ref(parameters.advanced.pseudo_family_parameters.functional)
    library = Ref(parameters.advanced.pseudo_family_parameters.library)
    accuracy = Ref(parameters.advanced.pseudo_family_parameters.accuracy)
    relativistic = Ref(parameters.advanced.pseudo_family_parameters.relativistic)
    ecutwfc = Ref(parameters.advanced.pw.parameters.SYSTEM.ecutwfc)
    ecutrho = Ref(parameters.advanced.pw.parameters.SYSTEM.ecutrho)

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

    family_link = solara.use_memo(
        lambda: "http://www.pseudo-dojo.org/"
        if library.value == "PseudoDojo"
        else f"https://www.materialscloud.org/discover/sssp/table/{accuracy.value}",
        [library.value, accuracy.value],
    )

    def get_pseudos_metadata(
        refresh: bool = False,
    ) -> tuple[dict[str, str], dict[str, list[float]], dict[str, str]]:
        structure = input_structure.value
        family = pseudo_family.value

        if not (structure and family):
            return {}, {"ecutwfc": [], "ecutrho": []}, {}

        family_node = family.get_node()
        cutoffs = family_node.get_cutoffs()
        unit = family_node.get_cutoffs_unit()

        filenames: dict[str, str] = {}
        cutoffs_dict: dict[str, list[float]] = {"ecutwfc": [], "ecutrho": []}
        resolved_pseudos: dict[str, str] = {}

        default_pseudos = (
            t.cast(
                dict[str, PseudoPotentialData],
                family_node.get_pseudos(structure=input_structure.value),
            )
            if refresh
            else {}
        )

        for kind in structure.kinds:
            if refresh:
                if not (pseudo := default_pseudos.get(kind.name)):
                    continue
            else:
                if not (uuid := pseudos.value.get(kind.name)):
                    continue
                pseudo = AiiDAService.get_pseudo(uuid)

            resolved_pseudos[kind.name] = pseudo.uuid
            filenames[kind.name] = pseudo.filename

            kind_cutoffs: dict = cutoffs.get(pseudo.element, {})
            kind_cutoffs_Ry = {
                key: U.Quantity(v, unit).to("Ry").to_tuple()[0]
                for key, v in kind_cutoffs.items()
            }
            cutoffs_dict["ecutwfc"].append(kind_cutoffs_Ry.get("cutoff_wfc", 0.0))
            cutoffs_dict["ecutrho"].append(kind_cutoffs_Ry.get("cutoff_rho", 0.0))

        return filenames, cutoffs_dict, resolved_pseudos

    filenames, cutoffs, _ = solara.use_memo(
        get_pseudos_metadata,
        [],
    )

    # Caches to avoid DB re-fetching and/or re-computation
    pseudo_filenames = solara.use_reactive(filenames)
    pseudo_cutoffs = solara.use_reactive(cutoffs)

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

    def set_accuracy():
        if disabled:
            return
        index = 1 if protocol.value == "stringent" else 0
        accuracy.set([*accuracy_options.keys()][index])

    def set_library_and_relativistic():
        if disabled:
            return
        library.set("PseudoDojo" if spin_orbit.value == "soc" else "SSSP")
        relativistic.set("FR" if spin_orbit.value == "soc" else "SR")

    def set_defaults():
        if disabled:
            return

        if not (input_structure.value and pseudo_family.value):
            return

        new_filenames, new_cutoffs, new_pseudos = get_pseudos_metadata(refresh=True)

        pseudo_filenames.set(new_filenames)
        pseudo_cutoffs.set(new_cutoffs)

        pseudos.set(new_pseudos)
        ecutwfc.set(max(new_cutoffs["ecutwfc"]))
        ecutrho.set(max(new_cutoffs["ecutrho"]))

    solara.use_effect(
        set_accuracy,
        [protocol.value, library.value],
    )

    solara.use_effect(
        set_library_and_relativistic,
        [spin_orbit.value],
    )

    solara.use_effect(
        set_defaults,
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
            disabled=disabled,
        )
        ToggleButtons(
            label="Library",
            options=library_options,
            value=library,
            disabled=disabled,
        )
        ToggleButtons(
            label="Accuracy",
            options=accuracy_options,
            value=accuracy,
            disabled=disabled,
        )

        with solara.Row(classes=["pseudo-cutoffs"]):
            solara.Text(
                "Cutoffs (Ry)",
                classes=["cutoffs-label"],
            )
            solara.InputText(
                label="ψ",
                value=ecutwfc,
                disabled=disabled,
                classes=["cutoff-input"],
            )
            solara.InputText(
                label="ρ",
                value=ecutrho,
                disabled=disabled,
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
                    cutoffs=(
                        pseudo_cutoffs.value["ecutwfc"][i],
                        pseudo_cutoffs.value["ecutrho"][i],
                    ),
                    update=update,
                    disabled=disabled,
                )

        with solara.Div(class_="pseudo-family-link"):
            solara.HTML(
                "span",
                f"Click <a href='{family_link}' target='_blank'>here</a> for more information about the selected pseudopotential family",
            )
