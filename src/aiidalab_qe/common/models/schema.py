from __future__ import annotations

import typing as t

from aiida.orm import ProcessNode, StructureData
from pydantic import BaseModel, ConfigDict

from aiidalab_qe.common.services.aiida import AiiDAService

# TODO dynamically "concatenate" announced plugin schemas
# TODO provide descriptions throughout
# TODO consider implementing model-level validation
# TODO consider using the models for UI selector options (dropdowns, toggles, etc.)
# TODO automate and simplify schema API


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class BasicModel(ConfiguredBaseModel):
    protocol: t.Literal[
        "fast",
        "moderate",
        "precise",
    ] = "moderate"
    spin_type: t.Literal[
        "none",
        "collinear",
    ] = "none"
    electronic_type: t.Literal[
        "metal",
        "insulator",
    ] = "metal"


class SystemModel(ConfiguredBaseModel):
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
    tot_magnetization: float = 0.0


class ControlModel(ConfiguredBaseModel):
    forc_conv_thr: float = 0.0
    etot_conv_thr: float = 0.0


class ElectronsModel(ConfiguredBaseModel):
    conv_thr: float = 0.0
    electron_maxstep: int = 80


class PwParametersModel(ConfiguredBaseModel):
    SYSTEM: SystemModel = SystemModel()
    CONTROL: ControlModel = ControlModel()
    ELECTRONS: ElectronsModel = ElectronsModel()


class PwModel(ConfiguredBaseModel):
    parameters: PwParametersModel = PwParametersModel()
    pseudos: dict[str, str] = {}


class HubbardParametersModel(ConfiguredBaseModel):
    hubbard_u: dict[str, float] = {}


class AdvancedModel(ConfiguredBaseModel):
    pw: PwModel = PwModel()
    clean_workdir: bool = False
    kpoints_distance: float = 0.0
    optimization_maxsteps: int = 50
    pseudo_family: str = ""
    hubbard_parameters: HubbardParametersModel = HubbardParametersModel()
    initial_magnetic_moments: dict[str, float] = {}


# class BandsModel(ConfiguredBaseModel):
#     projwfc_bands: t.Optional[bool] = None


# class PdosModel(ConfiguredBaseModel):
#     nscf_kpoints_distance: float = 0.1
#     use_pdos_degauss: bool = False
#     pdos_degauss: float = 0.005
#     energy_grid_step: float = 0.01


# class XasPseudosModel(ConfiguredBaseModel):
#     gipaw: str = ?
#     core_hole: str = ?


# class XasModel(ConfiguredBaseModel):
#     elements_list: list[str] = ?
#     core_hole_treatments: dict[str, str] = ?
#     pseudo_labels: dict[str, XasPseudosModel] = ?
#     core_wfc_data_labels: dict[str, str] = ?
#     supercell_min_parameter: float = ?


# class CorrectionEnergyModel(ConfiguredBaseModel):
#     exp: float = ?
#     core: float = ?


# class XpsModel(ConfiguredBaseModel):
#     structure_type: str = ?
#     pseudo_group: str = ?
#     correction_energies: dict[str, CorrectionEnergyModel] = ?
#     core_level_list: list[str] = ?


class CodeParallelizationModel(ConfiguredBaseModel):
    npools: t.Optional[int] = None


class CodeModel(ConfiguredBaseModel):
    # options: list[list[tuple[str, str]]] = ?
    code: str = ""
    nodes: int = 1
    cpus: int = 1
    ntasks_per_node: int = 1
    cpus_per_task: int = 1
    max_wallclock_seconds: int = 3600
    parallelization: CodeParallelizationModel = CodeParallelizationModel()


class CodesModel(ConfiguredBaseModel):
    override: t.Optional[bool] = None
    codes: dict[str, CodeModel] = {}


class ComputationalResourcesModel(ConfiguredBaseModel):
    global_: CodesModel = CodesModel()
    # bands: CodesModel
    # pdos: CodesModel
    # xas: CodesModel


class CalculationParametersModel(ConfiguredBaseModel):
    relax_type: t.Literal[
        "none",
        "positions",
        "positions_cell",
    ] = "positions_cell"
    properties: list[str] = []
    basic: BasicModel = BasicModel()
    advanced: AdvancedModel = AdvancedModel()
    # bands: BandsModel
    # pdos: PdosModel
    # xas: XasModel
    # xps: XpsModel


class QeAppModel(ConfiguredBaseModel):
    input_structure: t.Optional[StructureData] = None
    calculation_parameters: CalculationParametersModel = CalculationParametersModel()
    computational_resources: ComputationalResourcesModel = ComputationalResourcesModel()
    process: t.Optional[ProcessNode] = None


def from_process(pk: int | None) -> QeAppModel:
    from aiida.orm.utils.serialize import deserialize_unsafe

    try:
        process = AiiDAService.load_qe_app_workflow_node(pk)
        assert process
        ui_parameters = deserialize_unsafe(process.base.extras.get("ui_parameters", {}))
        assert ui_parameters
    except AssertionError:
        return QeAppModel()

    calculation_parameters = _extract_calculation_parameters(ui_parameters)
    computational_resources = _extract_computational_resources(ui_parameters)

    return QeAppModel(
        input_structure=process.inputs.structure,
        calculation_parameters=calculation_parameters,
        computational_resources=computational_resources,
        process=process,
    )


def _extract_calculation_parameters(parameters: dict) -> CalculationParametersModel:
    model = CalculationParametersModel()

    workchain_parameters: dict = parameters.get("workchain", {})
    model.relax_type = workchain_parameters.get("relax_type")

    models = {
        "basic": BasicModel,
        "advanced": AdvancedModel,
    }

    # TODO extand models by plugins

    for identifier, sub_model in models.items():
        if sub_model_parameters := parameters.get(identifier):
            setattr(model, identifier, sub_model(**sub_model_parameters))

    return model


def _extract_computational_resources(parameters: dict) -> ComputationalResourcesModel:
    return ComputationalResourcesModel(**parameters["codes"])
