import typing as t

import pydantic as pdt


class ConfiguredBaseModel(pdt.BaseModel):
    model_config = pdt.ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def get_options(cls, field_name: str):
        return t.get_args(cls.model_fields[field_name].annotation)
