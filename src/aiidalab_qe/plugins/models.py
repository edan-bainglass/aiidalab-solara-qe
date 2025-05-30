import typing as t

import solara
import pydantic as pdt

from aiidalab_qe.common.models.codes import ResourcesModel

PluginSettingsComponent = t.Callable[[pdt.BaseModel], solara.Element]


class PluginSettingsModel(pdt.BaseModel):
    model: pdt.BaseModel
    component: PluginSettingsComponent


class PluginResourcesModel(ResourcesModel):
    override: bool = False
