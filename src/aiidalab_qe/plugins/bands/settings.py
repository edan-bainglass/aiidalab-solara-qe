from __future__ import annotations

import typing as t

import solara
import solara.toestand

from aiidalab_qe.common.components.html import Paragraph
from aiidalab_qe.common.models.schema import CalculationParametersModel
from aiidalab_qe.common.types import StructureType

from .model import BandsSettingsModel as Model


@solara.component
def BandStructureSettings(
    active: bool,
    input_structure: solara.Reactive[StructureType],
    parameters: solara.Reactive[CalculationParametersModel],
):
    bands_settings = t.cast(Model, parameters.fields.plugins["bands"].model)
    projwfc_bands = solara.toestand.Ref(bands_settings.projwfc_bands)

    with solara.Div(
        class_=" ".join(
            [
                "control-group bands-settings",
                *(["d-none"] if not active else []),
            ],
        ),
    ):
        if not active:
            return

        print("\nrendering bands-settings component")

        with solara.Div(class_="plugin-info"):
            Paragraph("""
                The band structure workflow will automatically detect the
                default path in reciprocal space using the
                <a
                    href="https://www.materialscloud.org/work/tools/seekpath"
                    target="_blank"
                >SeeK-path tool</a>.
            """)
            Paragraph("""
                Fat Bands is a band structure plot that includes the angular
                momentum contributions from specific atoms or orbitals to each
                energy band. The thickness of the bands represents the strength
                of these contributions, providing insight into the electronic
                structure.
            """)
        solara.Checkbox(
            label="Fat bands",
            value=projwfc_bands,
        )
