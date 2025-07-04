from aiidalab_qe.common.models.codes import CodeModel, PwCodeModel

from ..models import PluginResourcesModel, PluginSettingsModel
from .bands import BandStructureSettings
from .model import BandsSettingsModel

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
                description="Projector wavefunction code",
                default_calcjob_plugin="quantumespresso.projwfc",
            ),
        },
    ),
}
