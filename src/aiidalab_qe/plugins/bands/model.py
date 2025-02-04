import typing as t

from aiidalab_qe.common.models.schema import ConfiguredBaseModel


class BandsSettingsModel(ConfiguredBaseModel):
    projwfc_bands: t.Optional[bool] = None
