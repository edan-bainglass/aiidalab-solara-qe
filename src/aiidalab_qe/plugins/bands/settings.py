from __future__ import annotations

import typing as t

import solara
from solara.toestand import Ref

from aiidalab_qe.common.components.html import Paragraph

from .model import BandsSettingsModel as Model

if t.TYPE_CHECKING:
    from aiidalab_qe.components.wizard.models import QeWizardModel


@solara.component
def BandStructureSettings(model: solara.Reactive[QeWizardModel]):
    calculation_parameters = model.fields.data.calculation_parameters
    bands_settings: Model = calculation_parameters.plugins["bands"].model  # type: ignore
    projwfc_bands = Ref(bands_settings.projwfc_bands)

    with solara.Div(class_="band-structure-settings"):
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
