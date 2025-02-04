import typing as t

from pydantic import Field

from .utils import ConfiguredBaseModel


class CodeModel(ConfiguredBaseModel):
    name: str = Field(exclude=True, default="")
    description: str = Field(exclude=True, default="")
    default_calcjob_plugin: str = Field(exclude=True, default="")

    code: str = ""
    nodes: int = 1
    cpus: int = 1
    ntasks_per_node: int = 1
    cpus_per_task: int = 1
    max_wallclock_seconds: int = 3600


class CodeParallelizationModel(ConfiguredBaseModel):
    npools: t.Optional[int] = None


class PwCodeModel(CodeModel):
    parallelization: CodeParallelizationModel = CodeParallelizationModel()


class ResourcesModel(ConfiguredBaseModel):
    codes: dict[str, CodeModel] = {}
