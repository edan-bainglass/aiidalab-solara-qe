import typing as t

import solara
from pydantic import BaseModel

from aiidalab_qe.common.models.codes import ResourcesModel

PluginSettingsComponent = t.Callable[[BaseModel], solara.Element]


class PluginSettingsModel(BaseModel):
    model: BaseModel
    component: PluginSettingsComponent


class PluginResourcesModel(ResourcesModel):
    override: bool = False
