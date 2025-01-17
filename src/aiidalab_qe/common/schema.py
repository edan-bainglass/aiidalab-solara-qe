from __future__ import annotations

import typing as t

from pydantic import BaseModel, ConfigDict, Field

from aiida import orm

# TODO dynamically "concatenate" announced plugin schemas
# TODO provide descriptions throughout
# TODO consider implementing model-level validation
# TODO consider using the models for UI selector options (dropdowns, toggles, etc.)


class ExcludeUnsetBaseModel(BaseModel):
    def model_dump(self, *args, **kwargs):
        kwargs.setdefault("exclude_unset", True)
        return super().model_dump(*args, **kwargs)


class BasicModel(BaseModel):
    protocol: t.Literal["fast", "moderate", "precise"]
    spin_type: t.Literal["none", "collinear"]
    electronic_type: t.Literal["metal", "insulator"]
    relax_type: t.Literal["none", "positions", "positions_cell"]
    properties: list[str]


class SystemModel(BaseModel):
    tot_charge: float
    starting_ns_eigenvalue: list[tuple[int, int, str, int]]
    ecutwfc: float
    ecutrho: float
    vdw_corr: t.Literal[
        "none",
        "dft-d3",
        "dft-d3bj",
        "dft-d3m",
        "dft-d3mbj",
        "ts-vdw",
    ]
    smearing: t.Literal[
        "cold",
        "gaussian",
        "fermi-dirac",
        "methfessel-paxton",
    ]
    degauss: float
    lspinorb: bool
    noncolin: bool
    nspin: int


class ControlModel(BaseModel):
    forc_conv_thr: float
    etot_conv_thr: float


class ElectronsModel(BaseModel):
    conv_thr: float
    electron_maxstep: int


class PwParametersModel(BaseModel):
    SYSTEM: SystemModel
    CONTROL: ControlModel
    ELECTRONS: ElectronsModel


class PwModel(BaseModel):
    parameters: PwParametersModel
    pseudos: dict[str, str]


class HubbardParametersModel(BaseModel):
    hubbard_u: dict[str, float]


class AdvancedModel(BaseModel):
    pw: PwModel
    clean_workdir: bool
    kpoints_distance: float
    optimization_maxsteps: int
    pseudo_family: str
    hubbard_parameters: HubbardParametersModel
    initial_magnetic_moments: dict[str, float]


# class BandsModel(BaseModel):
#     projwfc_bands: bool


# class PdosModel(BaseModel):
#     nscf_kpoints_distance: float
#     use_pdos_degauss: bool
#     pdos_degauss: float
#     energy_grid_step: float


# class XasPseudosModel(BaseModel):
#     gipaw: str
#     core_hole: str


# class XasModel(BaseModel):
#     elements_list: list[str]
#     core_hole_treatments: dict[str, str]
#     pseudo_labels: dict[str, XasPseudosModel]
#     core_wfc_data_labels: dict[str, str]
#     supercell_min_parameter: float


# class CorrectionEnergyModel(BaseModel):
#     exp: float
#     core: float


# class XpsModel(BaseModel):
#     structure_type: str
#     pseudo_group: str
#     correction_energies: dict[str, CorrectionEnergyModel]
#     core_level_list: list[str]


class CodeParallelizationModel(ExcludeUnsetBaseModel):
    npools: t.Optional[int]


class CodeModel(BaseModel):
    # options: list[list[tuple[str, str]]]
    code: str
    nodes: int
    cpus: int
    ntasks_per_node: int
    cpus_per_task: int
    max_wallclock_seconds: int
    parallelization: CodeParallelizationModel


class CodesModel(ExcludeUnsetBaseModel):
    override: t.Optional[bool]
    codes: dict[str, CodeModel]


class ComputationalResourcesModel(BaseModel):
    global_: CodesModel = Field(alias="global")
    # bands: CodesModel
    # pdos: CodesModel
    # xas: CodesModel


class CalculationParametersModel(BaseModel):
    basic: BasicModel
    advanced: AdvancedModel
    # bands: BandsModel
    # pdos: PdosModel
    # xas: XasModel
    # xps: XpsModel


class QeAppModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    input_structure: t.Optional[orm.StructureData] = None
    calculation_parameters: t.Optional[CalculationParametersModel] = None
    computational_resources: t.Optional[ComputationalResourcesModel] = None
    process: t.Optional[orm.ProcessNode] = None
