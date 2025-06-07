from aiidalab_qe.common.models.schema import ConfiguredBaseModel


class BandsSettingsModel(ConfiguredBaseModel):
    projwfc_bands: bool = False
