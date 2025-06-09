from aiidalab_qe.common.models.codes import CodeModel, PwCodeModel

from ..models import PluginResourcesModel, PluginSettingsModel
from .model import BandsSettingsModel
from .settings import BandStructureSettings
from .results import BandStructureResults

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
    "results": BandStructureResults,
}
