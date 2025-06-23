from aiidalab_qe.common.models.schema import Model


class PdosSettingsModel(Model):
    kpoints_distance: float = 0.1
    use_pdos_degauss: bool = False
    pdos_degauss: float = 0.005
    energy_grid_step: float = 0.01
