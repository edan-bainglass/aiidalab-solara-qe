from __future__ import annotations

import typing as t

from pydantic import BaseModel, ConfigDict, Field

from aiida import orm

# TODO dynamically "concatenate" announced plugin schemas
# TODO provide descriptions throughout
# TODO consider implementing model-level validation
# TODO consider using the models for UI selector options (dropdowns, toggles, etc.)


class BasicModel(BaseModel):
    protocol: t.Literal["fast", "moderate", "precise"] = "moderate"
    spin_type: t.Literal["none", "collinear"] = "none"
    electronic_type: t.Literal["metal", "insulator"] = "metal"


class SystemModel(BaseModel):
    tot_charge: float = 0.0
    starting_ns_eigenvalue: list[tuple[int, int, str, int]] = []
    ecutwfc: float = 0.0
    ecutrho: float = 0.0
    vdw_corr: t.Literal[
        "none",
        "dft-d3",
        "dft-d3bj",
        "dft-d3m",
        "dft-d3mbj",
        "ts-vdw",
    ] = "none"
    smearing: t.Literal[
        "cold",
        "gaussian",
        "fermi-dirac",
        "methfessel-paxton",
    ] = "cold"
    degauss: float = 0.0
    lspinorb: bool = False
    noncolin: bool = False
    nspin: int = 1


class ControlModel(BaseModel):
    forc_conv_thr: float = 0.0
    etot_conv_thr: float = 0.0


class ElectronsModel(BaseModel):
    conv_thr: float = 0.0
    electron_maxstep: int = 80


class PwParametersModel(BaseModel):
    SYSTEM: SystemModel = SystemModel()
    CONTROL: ControlModel = ControlModel()
    ELECTRONS: ElectronsModel = ElectronsModel()


class PwModel(BaseModel):
    parameters: PwParametersModel = PwParametersModel()
    pseudos: dict[str, str] = {}


class HubbardParametersModel(BaseModel):
    hubbard_u: dict[str, float] = {}


class AdvancedModel(BaseModel):
    pw: PwModel = PwModel()
    clean_workdir: bool = False
    kpoints_distance: float = 0.0
    optimization_maxsteps: int = 50
    pseudo_family: str = ""
    hubbard_parameters: HubbardParametersModel = HubbardParametersModel()
    initial_magnetic_moments: dict[str, float] = {}


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


class CodeParallelizationModel(BaseModel):
    npools: t.Optional[int] = None


class CodeModel(BaseModel):
    # options: list[list[tuple[str, str]]]
    code: str = ""
    nodes: int = 1
    cpus: int = 1
    ntasks_per_node: int = 1
    cpus_per_task: int = 1
    max_wallclock_seconds: int = 3600
    parallelization: CodeParallelizationModel = CodeParallelizationModel()


class CodesModel(BaseModel):
    override: t.Optional[bool] = None
    codes: dict[str, CodeModel] = {}


class ComputationalResourcesModel(BaseModel):
    global_: CodesModel = Field(alias="global", default=CodesModel())
    # bands: CodesModel
    # pdos: CodesModel
    # xas: CodesModel


class CalculationParametersModel(BaseModel):
    relax_type: t.Literal["none", "positions", "positions_cell"] = "positions_cell"
    properties: list[str] = []
    basic: BasicModel = BasicModel()
    advanced: AdvancedModel = AdvancedModel()
    # bands: BandsModel
    # pdos: PdosModel
    # xas: XasModel
    # xps: XpsModel


class QeAppModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    input_structure: t.Optional[orm.StructureData] = None
    calculation_parameters: CalculationParametersModel = CalculationParametersModel()
    computational_resources: ComputationalResourcesModel = ComputationalResourcesModel()
    process: t.Optional[orm.ProcessNode] = None
