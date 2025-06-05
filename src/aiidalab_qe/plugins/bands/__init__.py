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
            "pw": PwCodeModel(),
            "projwfc_bands": CodeModel(
                name="projwfc.x",
                description="Projector wavefunction code for band structures",
                default_calcjob_plugin="quantumespresso.projwfc",
            ),
        },
    ),
}
