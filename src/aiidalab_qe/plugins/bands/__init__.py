from aiidalab_qe.common.models.codes import CodeModel, PwCodeModel

from ..models import PluginResourcesModel, PluginSettingsModel
from .model import BandsSettingsModel
from .settings import BandStructureSettings

bands = {
    "title": "Electronic band structure",
    "settings": PluginSettingsModel(
        model=BandsSettingsModel(),
        component=BandStructureSettings,
    ),
    "resources": PluginResourcesModel(
        codes={
            "pw": PwCodeModel(
                name="pw.x",
                description="pw.x",
                default_calcjob_plugin="quantumespresso.pw",
            ),
            "projwfc_bands": CodeModel(
                name="projwfc.x",
                description="projwfc.x",
                default_calcjob_plugin="quantumespresso.projwfc",
            ),
        },
    ),
}
