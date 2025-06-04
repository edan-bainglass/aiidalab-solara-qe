from __future__ import annotations

import typing as t

import pydantic as pdt
from aiida.orm import ProcessNode, StructureData

from aiidalab_qe.common.services.aiida import AiiDAService
from aiidalab_qe.plugins.models import PluginResourcesModel, PluginSettingsModel
from aiidalab_qe.plugins.utils import get_plugin_resources, get_plugin_settings

from .codes import PwCodeModel, ResourcesModel
from .utils import ConfiguredBaseModel


class BasicSettingsModel(ConfiguredBaseModel):
    protocol: t.Literal[
        "fast",
        "balanced",
        "stringent",
    ] = "balanced"
    spin_type: t.Literal[
        "none",
        "collinear",
    ] = "none"
    electronic_type: t.Literal[
        "metal",
        "insulator",
    ] = "metal"


class SystemParametersModel(ConfiguredBaseModel):
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


class ControlParametersModel(ConfiguredBaseModel):
    forc_conv_thr: float = 0.0
    etot_conv_thr: float = 0.0


class ElectronsParametersModel(ConfiguredBaseModel):
    conv_thr: float = 0.0
    electron_maxstep: int = 80


class PwParametersModel(ConfiguredBaseModel):
    SYSTEM: SystemParametersModel = SystemParametersModel()
    CONTROL: ControlParametersModel = ControlParametersModel()
    ELECTRONS: ElectronsParametersModel = ElectronsParametersModel()


class PwModel(ConfiguredBaseModel):
    parameters: PwParametersModel = PwParametersModel()
    pseudos: dict[str, str] = {}


class HubbardParametersModel(ConfiguredBaseModel):
    hubbard_u: dict[str, float] = {}


class AdvancedSettingsModel(ConfiguredBaseModel):
    pw: PwModel = PwModel()
    clean_workdir: bool = False
    kpoints_distance: float = 0.0
    optimization_maxsteps: int = 50
    pseudo_family: str = ""
    hubbard_parameters: HubbardParametersModel = HubbardParametersModel()
    initial_magnetic_moments: t.Optional[dict[str, float]] = None


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


class CalculationParametersModel(ConfiguredBaseModel):
    relax_type: t.Literal[
        "none",
        "positions",
        "positions_cell",
    ] = "positions_cell"
    properties: list[str] = []
    basic: BasicSettingsModel = BasicSettingsModel()
    advanced: AdvancedSettingsModel = AdvancedSettingsModel()
    plugins: dict[str, PluginSettingsModel] = {}

    @pdt.model_validator(mode="before")
    @classmethod
    def _fetch_plugins(cls, data: t.Any) -> t.Any:
        plugin_data = data.get("plugins", {})
        for plugin, settings in get_plugin_settings().items():
            if plugin not in plugin_data:
                plugin_data[plugin] = settings
        data["plugins"] = plugin_data
        return data


class ComputationalResourcesModel(ConfiguredBaseModel):
    active: str = "global"
    global_: ResourcesModel = ResourcesModel(
        codes={
            "pw": PwCodeModel(),
        }
    )
    plugins: dict[str, PluginResourcesModel] = {}

    @pdt.model_validator(mode="before")
    @classmethod
    def _fetch_plugins(cls, data: t.Any) -> t.Any:
        plugin_data = data.get("plugins", {})
        for plugin, resources in get_plugin_resources().items():
            if plugin not in plugin_data:
                plugin_data[plugin] = resources
        data["plugins"] = plugin_data
        return data


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
        "basic": BasicSettingsModel,
        "advanced": AdvancedSettingsModel,
    }

    # TODO extend models by plugins

    for identifier, sub_model in models.items():
        if sub_model_parameters := parameters.get(identifier):
            setattr(model, identifier, sub_model(**sub_model_parameters))

    return model


def _extract_computational_resources(parameters: dict) -> ComputationalResourcesModel:
    return ComputationalResourcesModel(**parameters["codes"])
