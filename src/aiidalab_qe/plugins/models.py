import pydantic as pdt

from aiidalab_qe.common.models.codes import ResourcesModel

from .types import PluginSettingsComponent


class PluginSettingsModel(pdt.BaseModel):
    model: pdt.BaseModel
    component: PluginSettingsComponent


class PluginResourcesModel(ResourcesModel):
    override: bool = False
