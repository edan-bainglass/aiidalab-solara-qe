import typing as t

import pydantic as pdt

from aiidalab_qe.common.services.aiida import AiiDAService

from .utils import ConfiguredBaseModel


class CodeModel(ConfiguredBaseModel):
    name: str = pdt.Field(exclude=True, default="")
    description: str = pdt.Field(exclude=True, default="")
    default_calcjob_plugin: str = pdt.Field(exclude=True, default="")

    code: str = ""
    nodes: int = 1
    cpus: int = 1
    ntasks_per_node: int = 1
    cpus_per_task: int = 1
    max_wallclock_seconds: int = 3600

    @property
    def code_uuid(self) -> str:
        try:
            return AiiDAService.load_code(self.code).uuid
        except Exception:
            return ""

    @pdt.field_validator("code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        try:
            code = AiiDAService.load_code(value)
            return code.full_label
        except Exception:
            return ""

    def get_model_state(self) -> dict[str, t.Any]:
        return {
            "code": self.code_uuid,
            "nodes": self.nodes,
            "cpus": self.cpus,
            "ntasks_per_node": self.ntasks_per_node,
            "cpus_per_task": self.cpus_per_task,
            "max_wallclock_seconds": self.max_wallclock_seconds,
        }

    def get_suffix(self) -> str:
        return self.default_calcjob_plugin.split(".")[-1]


class CodeParallelizationModel(ConfiguredBaseModel):
    npools: t.Optional[int] = None


class PwCodeModel(CodeModel):
    name: str = "pw.x"
    description: str = "Plane-wave self-consistent field (SCF) code"
    default_calcjob_plugin: str = "quantumespresso.pw"

    parallelization: CodeParallelizationModel = CodeParallelizationModel()

    def get_model_state(self) -> dict[str, t.Any]:
        return {
            **super().get_model_state(),
            "parallelization": self.parallelization.model_dump(exclude_unset=True),
        }


class ResourcesModel(ConfiguredBaseModel):
    codes: dict[str, CodeModel] = {}
