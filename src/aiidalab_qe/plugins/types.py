import typing as t

import pydantic as pdt
import solara

from aiidalab_qe.common.types import ProcessType

PluginSettingsComponent = t.Callable[
    [bool, solara.Reactive[pdt.BaseModel]],
    solara.Element,
]

PluginResultsComponent = t.Callable[
    [ProcessType],
    solara.Element,
]
