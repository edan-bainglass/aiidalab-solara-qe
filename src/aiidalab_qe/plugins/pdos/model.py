import typing as t

from aiidalab_qe.common.models.schema import ConfiguredBaseModel


class PdosSettingsModel(ConfiguredBaseModel):
    kpoints_distance: float = 0.1
    mesh_grid: t.Optional[str] = ""
    use_pdos_degauss: bool = False
    pdos_degauss: float = 0.005
    energy_grid_step: float = 0.01
