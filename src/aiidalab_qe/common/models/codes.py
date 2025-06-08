import typing as t

import pydantic as pdt

from aiidalab_qe.common.services.aiida import AiiDAService

from .utils import ConfiguredBaseModel


class CodeModel(ConfiguredBaseModel):
    name: str = pdt.Field("", exclude=True)
    description: str = pdt.Field("", exclude=True)
    default_calcjob_plugin: str = pdt.Field("", exclude=True)

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
        except Exception as err:
            print(f"Error loading code: {err}")
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
            **self.model_dump(exclude_none=True),
            "code": self.code_uuid,
        }

    def get_suffix(self) -> str:
        return self.default_calcjob_plugin.split(".")[-1]

    def update_and_validate(self, data: dict[str, t.Any]) -> "CodeModel":
        """Update the model with validated data.

        Parameters
        ----------
        `data` : `dict[str, t.Any]`
            The data to update the model with.

        Returns
        -------
        `CodeModel`
            A new instance of the model with updated and validated data.
        """
        return self.model_copy(
            update=self.model_validate(
                self.model_copy(update=data).model_dump()
            ).model_dump()
        )


class CodeParallelizationModel(ConfiguredBaseModel):
    npools: t.Optional[int] = None


class PwCodeModel(CodeModel):
    parallelization: CodeParallelizationModel = CodeParallelizationModel()

    def __init__(self, **data: t.Any):
        super().__init__(**data)
        self.name = "pw.x"
        self.description = "Plane-wave self-consistent field (SCF) code"
        self.default_calcjob_plugin = "quantumespresso.pw"

    def get_model_state(self) -> dict[str, t.Any]:
        return {
            **super().get_model_state(),
            "parallelization": self.parallelization.model_dump(exclude_none=True),
        }


class CodeModelFactory:
    @staticmethod
    def from_serialized(code_key: str, serialized: dict) -> CodeModel:
        code_model_class = PwCodeModel if code_key == "pw" else CodeModel
        return code_model_class(**serialized)


class ResourcesModel(ConfiguredBaseModel):
    codes: dict[str, CodeModel] = pdt.Field(default_factory=dict)
