from aiidalab_qe.common.models.codes import CodeModel, PwCodeModel

from ..models import PluginResourcesModel, PluginSettingsModel
from .model import PdosSettingsModel
from .pdos import PdosSettings

pdos = {
    "title": "Electronic projected density of states (PDOS)",
    "settings": PluginSettingsModel(
        model=PdosSettingsModel(),
        component=PdosSettings,
    ),
    "resources": PluginResourcesModel(
        codes={
            "pw": PwCodeModel(),
            "dos": CodeModel(
                name="dos.x",
                description="Density of states code",
                default_calcjob_plugin="quantumespresso.dos",
            ),
            "projwfc": CodeModel(
                name="projwfc.x",
                description="Projector wavefunction code",
                default_calcjob_plugin="quantumespresso.projwfc",
            ),
        },
    ),
}
