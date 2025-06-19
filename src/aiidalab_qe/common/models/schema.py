from __future__ import annotations

import typing as t

import pydantic as pdt
from aiida.orm import ProcessNode, StructureData

from aiidalab_qe.common.services.aiida import AiiDAService
from aiidalab_qe.plugins.models import PluginResourcesModel, PluginSettingsModel
from aiidalab_qe.plugins.utils import get_plugin_resources, get_plugin_settings

from .codes import CodeModelFactory, PwCodeModel, ResourcesModel
from .utils import ConfiguredBaseModel


class BasicSettingsModel(ConfiguredBaseModel):
    electronic_type: t.Literal[
        "metal",
        "insulator",
    ] = "metal"
    spin_type: t.Literal[
        "none",
        "collinear",
    ] = "none"
    spin_orbit: t.Annotated[
        t.Literal[
            "wo_soc",
            "soc",
        ],
        pdt.Field(exclude=True),
    ] = "wo_soc"
    protocol: t.Literal[
        "fast",
        "balanced",
        "stringent",
    ] = "balanced"


EigenvalueType = tuple[int, int, str, float]


class SystemParametersModel(ConfiguredBaseModel):
    tot_charge: float = 0.0
    starting_ns_eigenvalue: t.Optional[list[EigenvalueType]] = None
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
    pseudos: dict[str, str] = pdt.Field(default_factory=dict)


class HubbardParametersModel(ConfiguredBaseModel):
    use_hubbard_u: t.Annotated[bool, pdt.Field(exclude=True)] = False
    use_eigenvalues: t.Annotated[bool, pdt.Field(exclude=True)] = False
    hubbard_u: dict[str, float] = {}
    eigenvalues: list[list[list[EigenvalueType]]] = []


MagneticMomentsType = dict[str, float]


class AdvancedSettingsModel(ConfiguredBaseModel):
    pw: PwModel = PwModel()
    clean_workdir: bool = False
    kpoints_distance: float = 0.0
    optimization_maxsteps: int = 50
    pseudo_family: str = "SSSP/1.3/PBEsol/efficiency"
    hubbard_parameters: HubbardParametersModel = HubbardParametersModel()
    initial_magnetic_moments: MagneticMomentsType = pdt.Field(default_factory=dict)


class CalculationParametersModel(ConfiguredBaseModel):
    relax_type: t.Literal[
        "none",
        "positions",
        "positions_cell",
    ] = "positions_cell"
    basic: BasicSettingsModel = BasicSettingsModel()
    advanced: AdvancedSettingsModel = AdvancedSettingsModel()
    plugins: dict[str, PluginSettingsModel] = pdt.Field(default_factory=dict)

    @pdt.model_validator(mode="before")
    @classmethod
    def _fetch_plugins(cls, data: dict[str, t.Any]) -> t.Any:
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
    plugins: dict[str, PluginResourcesModel] = pdt.Field(default_factory=dict)
    plugin_mapping: dict[str, str] = pdt.Field(default_factory=dict, exclude=True)

    @pdt.model_validator(mode="before")
    @classmethod
    def _fetch_plugins(cls, data: dict[str, t.Any]) -> t.Any:
        plugins = data.get("plugins", {})
        mapping = data.get("plugin_mapping", {})
        for plugin, resources in get_plugin_resources().items():
            if plugin not in plugins:
                plugins[plugin] = resources
                for code, model in resources.codes.items():
                    if code not in mapping:
                        mapping[code] = model.default_calcjob_plugin.split(".")[-1]
        data["plugin_mapping"] = mapping
        data["plugins"] = plugins
        return data


class QeAppModel(ConfiguredBaseModel):
    label: str = "New workflow"
    description: str = ""
    input_structure: t.Optional[StructureData] = None
    properties: list[str] = pdt.Field(default_factory=list)
    calculation_parameters: CalculationParametersModel = CalculationParametersModel()
    computational_resources: ComputationalResourcesModel = ComputationalResourcesModel()
    process: t.Optional[ProcessNode] = None

    def to_legacy_parameters(self) -> dict:
        parameters = self.calculation_parameters
        resources = self.computational_resources
        legacy_parameters = {
            "workchain": {
                "protocol": parameters.basic.protocol,
                "spin_type": parameters.basic.spin_type,
                "electronic_type": parameters.basic.electronic_type,
                "relax_type": parameters.relax_type,
                "properties": ["relax", *self.properties],
            },
            "advanced": {
                **parameters.advanced.model_dump(exclude_none=True),
            },
            **{
                plugin: settings.model.model_dump(exclude_none=True)
                for plugin, settings in parameters.plugins.items()
                if plugin in self.properties
            },
            "codes": {
                "global": {
                    "codes": {
                        f"quantumespresso__{code.get_suffix()}": code.get_model_state()
                        for code in resources.global_.codes.values()
                    }
                },
                **{
                    plugin: {
                        "override": plugin_resources.override,
                        **{
                            "codes": {
                                code: model.get_model_state()
                                if plugin_resources.override
                                else resources.global_.codes.get(
                                    resources.plugin_mapping[code]
                                ).get_model_state()
                                for code, model in plugin_resources.codes.items()
                            }
                        },
                    }
                    for plugin, plugin_resources in resources.plugins.items()
                    if plugin in self.properties
                },
            },
        }
        if parameters.basic.spin_orbit == "soc":
            legacy_parameters["advanced"]["pw"]["parameters"]["SYSTEM"] |= {
                "lspinorb": True,
                "noncolin": True,
                "nspin": 4,
            }
        return legacy_parameters

    @classmethod
    def from_process(cls, pk: t.Optional[int], lock: bool = True) -> QeAppModel:
        from aiida.orm.utils.serialize import deserialize_unsafe

        ui_parameters: dict[str, t.Any]

        try:
            process = AiiDAService.load_qe_app_workflow_node(pk)
            assert process
            ui_parameters = deserialize_unsafe(
                process.base.extras.get("ui_parameters", {})
            )
            assert ui_parameters
        except AssertionError as err:
            print(f"Error loading process with pk={pk}: {err}")
            return QeAppModel()

        properties = ui_parameters.get("workchain", {}).pop("properties", [])
        codes = ui_parameters.pop("codes", {})
        calculation_parameters = _extract_calculation_parameters(ui_parameters)
        computational_resources = _extract_computational_resources(codes)

        return cls(
            label=process.label or "New workflow",
            description=process.description or "",
            input_structure=process.inputs.structure,
            properties=properties,
            calculation_parameters=calculation_parameters,
            computational_resources=computational_resources,
            process=process,
        )


# TODO needs attention!
def _extract_calculation_parameters(parameters: dict) -> CalculationParametersModel:
    model = CalculationParametersModel()
    workchain_parameters: dict = parameters.pop("workchain", {})
    model.relax_type = workchain_parameters.pop("relax_type")
    model.basic = BasicSettingsModel(**workchain_parameters)
    advanced_parameters = parameters.pop("advanced", {})
    model.basic.spin_orbit = (
        "soc"
        if advanced_parameters.get("pw", {})
        .get("parameters", {})
        .get("SYSTEM", {})
        .get("lspinorb")
        else "wo_soc"
    )
    model.advanced = AdvancedSettingsModel(**advanced_parameters)
    plugins = get_plugin_settings()
    model.plugins = {
        plugin: PluginSettingsModel(
            model=plugins[plugin].model.model_validate(data),
            component=plugins[plugin].component,
        )
        for plugin, data in parameters.items()
    }
    return model


CodesParams = dict[str, dict[str, dict[str, t.Any]]]


def _extract_computational_resources(codes: CodesParams) -> ComputationalResourcesModel:
    computational_resources = ComputationalResourcesModel()
    global_codes = {
        (
            key := code_key.replace("quantumespresso__", "")
        ): CodeModelFactory.from_serialized(key, code_model)
        for code_key, code_model in codes.pop("global", {}).get("codes", {}).items()
    }
    computational_resources.global_ = ResourcesModel(
        codes=global_codes
        or {
            "pw": PwCodeModel(),
        }
    )
    plugin_resources = get_plugin_resources()
    computational_resources.plugins = {
        plugin: plugin_resources[plugin].model_validate(
            {
                "override": resources.get("override", False),
                "codes": {
                    code: plugin_resources[plugin].codes[code].update_and_validate(data)
                    for code, data in sorted(
                        resources.get("codes", {}).items(),
                        key=lambda item: item[0] != "pw",  # False < True
                    )
                },
            }
        )
        for plugin, resources in codes.items()
        if plugin in plugin_resources
    }
    return computational_resources
