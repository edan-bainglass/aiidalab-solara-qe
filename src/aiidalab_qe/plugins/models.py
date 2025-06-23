import pydantic as pdt

from aiidalab_qe.common.models.codes import ResourcesModel
from aiidalab_qe.common.models.utils import Model

from .types import PluginSettingsComponent


class PluginSettingsModel(pdt.BaseModel):
    model: Model
    component: PluginSettingsComponent


class PluginResourcesModel(ResourcesModel):
    override: bool = False
