from __future__ import annotations

import typing as t

import numpy as np
import pydantic as pdt

from aiidalab_qe.common.services.aiida import AiiDAService, PseudoFamilyNode
from aiidalab_qe.common.types import StructureType
from aiidalab_qe.plugins.models import PluginResourcesModel, PluginSettingsModel
from aiidalab_qe.plugins.utils import get_plugin_resources, get_plugin_settings

from .codes import CodeModelFactory, PwCodeModel, ResourcesModel
from .utils import ConfiguredBaseModel

PROTOCOL_MAP = {
    "moderate": "balanced",
    "precise": "stringent",
}


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
    eigenvalues: t.Annotated[
        list[list[list[EigenvalueType]]],
        pdt.Field(exclude=True),
    ] = []
    """Starting eigenvalues for Hubbard U formatted as
    [[[state, spin, kind_name, eigenvalue], ...], ...]
    for ease of use in the UI."""


class PseudoFamilyParametersModel(ConfiguredBaseModel):
    versions: dict[str, str] = {
        "SSSP": "1.3",
        "PseudoDojo": "0.4",
    }
    functional: t.Literal[
        "PBE",
        "PBEsol",
    ] = "PBEsol"
    version: str = "1.3"
    library: t.Literal[
        "SSSP",
        "PseudoDojo",
    ] = "SSSP"
    accuracy: t.Literal[
        "efficiency",
        "precision",
        "standard",
        "stringent",
    ] = "efficiency"
    relativistic: t.Optional[t.Literal["SR", "FR"]] = None
    file_type: t.Optional[t.Literal["upf"]] = None

    @classmethod
    def from_string(cls, pseudo_family_string: str) -> PseudoFamilyParametersModel:
        library = pseudo_family_string.split("/")[0]
        if library == "SSSP":
            version, functional, accuracy = pseudo_family_string.split("/")[1:]
            relativistic = None
            file_type = None
        elif library == "PseudoDojo":
            (
                version,
                functional,
                relativistic,
                accuracy,
                file_type,
            ) = pseudo_family_string.split("/")[1:]
        else:
            raise ValueError(
                f"Not able to parse valid library name from {pseudo_family_string}"
            )

        return cls(
            library=library,
            version=version,
            functional=functional,
            accuracy=accuracy,
            relativistic=relativistic,
            file_type=file_type,
        )

    def to_string(self) -> str:
        prefix = f"{self.library}/{self.versions.get(self.library)}"
        if self.library == "PseudoDojo":
            suffix = f"{self.functional}/{self.relativistic}/{self.accuracy}/upf"
        elif self.library == "SSSP":
            suffix = f"{self.functional}/{self.accuracy}"
        return f"{prefix}/{suffix}"

    def get_node(self) -> t.Optional[PseudoFamilyNode]:
        """Get the pseudo family node from AiiDA."""
        if not self.library or not self.functional:
            return None
        pseudo_family_string = self.to_string()
        return AiiDAService.load_pseudo_family(pseudo_family_string)  # type: ignore


MagneticMomentsType = t.Optional[dict[str, float]]


class AdvancedSettingsModel(ConfiguredBaseModel):
    pw: PwModel = PwModel()
    clean_workdir: bool = False
    kpoints_distance: float = 0.0
    optimization_maxsteps: int = 50
    pseudo_family: str = "SSSP/1.3/PBEsol/efficiency"
    pseudo_family_parameters: t.Annotated[
        PseudoFamilyParametersModel,
        pdt.Field(exclude=True),
    ] = PseudoFamilyParametersModel()
    hubbard_parameters: HubbardParametersModel = HubbardParametersModel()
    initial_magnetic_moments: MagneticMomentsType = pdt.Field(default_factory=dict)

    @pdt.model_validator(mode="after")
    def update_pseudo_family_parameters(self) -> AdvancedSettingsModel:
        if self.pseudo_family:
            parameters = PseudoFamilyParametersModel.from_string(self.pseudo_family)
            self.pseudo_family_parameters = parameters
        return self


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
    input_structure: t.Optional[StructureType] = None
    properties: list[str] = pdt.Field(default_factory=list)
    calculation_parameters: CalculationParametersModel = CalculationParametersModel()
    computational_resources: ComputationalResourcesModel = ComputationalResourcesModel()
    process: t.Optional[str] = None

    def to_legacy_parameters(self) -> dict:
        parameters = self.calculation_parameters
        resources = self.computational_resources

        legacy_parameters = {
            "workchain": {
                "protocol": parameters.basic.protocol,
                "spin_type": parameters.basic.spin_type,
                "electronic_type": parameters.basic.electronic_type,
                "relax_type": parameters.relax_type,
                "properties": ["relax", *self.properties],  # TODO relax always?
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

        # SOC
        # TODO consider doing this in a model validator
        if parameters.basic.spin_orbit == "soc":
            legacy_parameters["advanced"]["pw"]["parameters"]["SYSTEM"] |= {
                "lspinorb": True,
                "noncolin": True,
                "nspin": 4,
            }

        # Hubbard U
        # TODO consider doing this in a model validator
        if eigenvalues := parameters.advanced.hubbard_parameters.eigenvalues:
            starting_ns_eigenvalue = convert_eigenvalues_to_qe_format(eigenvalues)
            legacy_parameters["advanced"]["pw"]["parameters"]["SYSTEM"] |= {
                "starting_ns_eigenvalue": starting_ns_eigenvalue,
            }

        return legacy_parameters

    @classmethod
    def from_model(cls, model: QeAppModel):
        return model.model_copy(deep=True, update={"process": None})

    @classmethod
    def from_process(cls, pk: t.Optional[int]) -> QeAppModel:
        from aiida.orm.utils.serialize import deserialize_unsafe

        ui_parameters: dict[str, t.Any]

        try:
            process = AiiDAService.load_qe_app_workflow_node(pk)
            assert process, f"Process with pk={pk} not found"
            ui_parameters = process.base.extras.get("ui_parameters", {})
            ui_parameters = deserialize_unsafe(ui_parameters)
            assert ui_parameters, f"UI parameters for process with pk={pk} not found"
        except Exception as err:
            print(f"Error loading process with pk={pk}: {err}")
            # TODO show error in UI and return nothing
            return QeAppModel()

        properties = [
            *filter(
                lambda p: p != "relax",
                ui_parameters.get("workchain", {}).pop("properties", []),
            )
        ]
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
            process=process.uuid,
        )


def _extract_calculation_parameters(parameters: dict) -> CalculationParametersModel:
    model = CalculationParametersModel()

    basic: dict = parameters.pop("workchain", {})
    advanced: dict = parameters.pop("advanced", {})

    model.relax_type = basic.pop("relax_type")
    include_soc = advanced["pw"]["parameters"]["SYSTEM"].get("lspinorb", False)
    basic["spin_orbit"] = "soc" if include_soc else "wo_soc"
    basic["protocol"] = PROTOCOL_MAP.get(basic["protocol"], basic["protocol"])
    model.basic = BasicSettingsModel(**basic)

    # Magnetization
    # TODO consider doing this in a model validator
    moments = advanced.get("initial_magnetic_moments", {})
    advanced["initial_magnetic_moments"] = moments

    # Hubbard U
    # TODO consider doing this in a model validator
    if "hubbard_parameters" in advanced:
        advanced["hubbard_parameters"]["use_hubbard_u"] = True
        system_parameters = advanced["pw"]["parameters"]["SYSTEM"]
        if starting_ns_eigenvalue := system_parameters.get("starting_ns_eigenvalue"):
            eigenvalues = convert_eigenvalues_to_ui_format(starting_ns_eigenvalue)
            advanced["hubbard_parameters"]["eigenvalues"] = eigenvalues
            advanced["hubbard_parameters"]["use_eigenvalues"] = True

    model.advanced = AdvancedSettingsModel(**advanced)

    plugins = get_plugin_settings()
    model.plugins = {
        plugin: PluginSettingsModel(
            model=plugins[plugin].model.model_validate(data),
            component=plugins[plugin].component,
        )
        for plugin, data in parameters.items()
    }

    return model


def convert_eigenvalues_to_ui_format(
    eigenvalues: list[EigenvalueType],
) -> list[list[list[EigenvalueType]]]:
    eigenvalues_array = np.array(eigenvalues, dtype=object)
    num_states = len(set(eigenvalues_array[:, 0]))
    num_spins = len(set(eigenvalues_array[:, 1]))
    num_kinds = len(set(eigenvalues_array[:, 2]))
    new_shape = (num_kinds, num_spins, num_states, 4)
    return eigenvalues_array.reshape(new_shape).tolist()


def convert_eigenvalues_to_qe_format(
    eigenvalues: list[list[list[EigenvalueType]]],
) -> list[EigenvalueType]:
    # TODO double-check the conversion logic
    eigenvalues_array = np.array(eigenvalues, dtype=object)
    new_shape = (int(np.prod(eigenvalues_array.shape[:-1])), 4)
    return [
        tuple(eigenvalue)
        for eigenvalue in eigenvalues_array.reshape(new_shape).tolist()
    ]


CodesParams = dict[str, dict[str, dict[str, t.Any]]]


def _extract_computational_resources(codes: CodesParams) -> ComputationalResourcesModel:
    computational_resources = ComputationalResourcesModel()
    global_codes = {
        (
            key := code_key.replace("quantumespresso__", "")
        ): CodeModelFactory.from_serialized(key, code_model)
        for code_key, code_model in codes.pop("global", {}).get("codes", {}).items()
    }
    computational_resources.global_ = ResourcesModel(codes=global_codes)
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
