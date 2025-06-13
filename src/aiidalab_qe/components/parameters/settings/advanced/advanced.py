from __future__ import annotations

import solara
from solara.toestand import Ref

from aiidalab_qe.common.models.schema import CalculationParametersModel


@solara.component
def AdvancedSettings(parameters: solara.Reactive[CalculationParametersModel]):
    advanced_settings = parameters.fields.advanced
