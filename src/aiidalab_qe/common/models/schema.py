from __future__ import annotations

import typing as t

from aiida.orm import ProcessNode, StructureData
from solara import Reactive, reactive

from aiidalab_qe.common.services.aiida import AiiDAService

from .reactive import ReactiveDataclass

# TODO dynamically "concatenate" announced plugin schemas
# TODO provide descriptions throughout
# TODO consider implementing model-level validation
# TODO consider using the models for UI selector options (dropdowns, toggles, etc.)
# TODO automate and simplify schema API


class BasicModel(ReactiveDataclass):
    protocol: Reactive[
        t.Literal[
            "fast",
            "moderate",
            "precise",
        ]
    ] = reactive("moderate")
    spin_type: Reactive[
        t.Literal[
            "none",
            "collinear",
        ]
    ] = reactive("none")
    electronic_type: Reactive[
        t.Literal[
            "metal",
            "insulator",
        ]
    ] = reactive("metal")


class SystemModel(ReactiveDataclass):
    tot_charge: Reactive[float] = reactive(0.0)
    starting_ns_eigenvalue: list[tuple[int, int, str, int]] = []
    ecutwfc: Reactive[float] = reactive(0.0)
    ecutrho: Reactive[float] = reactive(0.0)
    vdw_corr: Reactive[
        t.Literal[
            "none",
            "dft-d3",
            "dft-d3bj",
            "dft-d3m",
            "dft-d3mbj",
            "ts-vdw",
        ]
    ] = reactive("none")
    smearing: Reactive[
        t.Literal[
            "cold",
            "gaussian",
            "fermi-dirac",
            "methfessel-paxton",
        ]
    ] = reactive("cold")
    degauss: Reactive[float] = reactive(0.0)
    lspinorb: Reactive[bool] = reactive(False)
    noncolin: Reactive[bool] = reactive(False)
    nspin: Reactive[int] = reactive(1)
    tot_magnetization: Reactive[float] = reactive(0.0)


class ControlModel(ReactiveDataclass):
    forc_conv_thr: Reactive[float] = reactive(0.0)
    etot_conv_thr: Reactive[float] = reactive(0.0)


class ElectronsModel(ReactiveDataclass):
    conv_thr: Reactive[float] = reactive(0.0)
    electron_maxstep: Reactive[int] = reactive(80)


class PwParametersModel(ReactiveDataclass):
    SYSTEM: SystemModel = SystemModel()
    CONTROL: ControlModel = ControlModel()
    ELECTRONS: ElectronsModel = ElectronsModel()


class PwModel(ReactiveDataclass):
    parameters: PwParametersModel = PwParametersModel()
    pseudos: Reactive[dict[str, str]] = reactive({})


class HubbardParametersModel(ReactiveDataclass):
    hubbard_u: Reactive[dict[str, float]] = reactive({})


class AdvancedModel(ReactiveDataclass):
    pw: PwModel = PwModel()
    clean_workdir: Reactive[bool] = reactive(False)
    kpoints_distance: Reactive[float] = reactive(0.0)
    optimization_maxsteps: Reactive[int] = reactive(50)
    pseudo_family: Reactive[str] = reactive("")
    hubbard_parameters: HubbardParametersModel = HubbardParametersModel()
    initial_magnetic_moments: Reactive[dict[str, float]] = reactive({})


# class BandsModel(ReactiveDataclass):
#     projwfc_bands: Reactive[bool | None] = reactive(None)


# class PdosModel(ReactiveDataclass):
#     nscf_kpoints_distance: Reactive[float] = reactive(0.1)
#     use_pdos_degauss: Reactive[bool] = reactive(False)
#     pdos_degauss: Reactive[float] = reactive(0.005)
#     energy_grid_step: Reactive[float] = reactive(0.01)


# class XasPseudosModel(ReactiveDataclass):
#     gipaw: str = ?
#     core_hole: str = ?


# class XasModel(ReactiveDataclass):
#     elements_list: list[str] = ?
#     core_hole_treatments: dict[str, str] = ?
#     pseudo_labels: dict[str, XasPseudosModel] = ?
#     core_wfc_data_labels: dict[str, str] = ?
#     supercell_min_parameter: Reactive[float] = ?


# class CorrectionEnergyModel(ReactiveDataclass):
#     exp: Reactive[float] = ?
#     core: Reactive[float] = ?


# class XpsModel(ReactiveDataclass):
#     structure_type: str = ?
#     pseudo_group: str = ?
#     correction_energies: dict[str, CorrectionEnergyModel] = ?
#     core_level_list: list[str] = ?


class CodeParallelizationModel(ReactiveDataclass):
    npools: Reactive[int | None] = reactive(None)


class CodeModel(ReactiveDataclass):
    # options: list[list[tuple[str, str]]] = ?
    code: Reactive[str] = reactive("")
    nodes: Reactive[int] = reactive(1)
    cpus: Reactive[int] = reactive(1)
    ntasks_per_node: Reactive[int] = reactive(1)
    cpus_per_task: Reactive[int] = reactive(1)
    max_wallclock_seconds: Reactive[int] = reactive(3600)
    parallelization: CodeParallelizationModel = CodeParallelizationModel()


class CodesModel(ReactiveDataclass):
    override: Reactive[bool | None] = reactive(None)
    codes: Reactive[dict[str, CodeModel]] = reactive({})


class ComputationalResourcesModel(ReactiveDataclass):
    global_: CodesModel = CodesModel()
    # bands: CodesModel
    # pdos: CodesModel
    # xas: CodesModel


class CalculationParametersModel(ReactiveDataclass):
    relax_type: Reactive[
        t.Literal[
            "none",
            "positions",
            "positions_cell",
        ]
    ] = reactive("positions_cell")
    properties: Reactive[list[str]] = reactive([])
    basic: BasicModel = BasicModel()
    advanced: AdvancedModel = AdvancedModel()
    # bands: BandsModel
    # pdos: PdosModel
    # xas: XasModel
    # xps: XpsModel


class QeAppModel(ReactiveDataclass):
    input_structure: Reactive[StructureData | None] = reactive(None)
    calculation_parameters: CalculationParametersModel = CalculationParametersModel()
    computational_resources: ComputationalResourcesModel = ComputationalResourcesModel()
    process: Reactive[ProcessNode | None] = reactive(None)


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
