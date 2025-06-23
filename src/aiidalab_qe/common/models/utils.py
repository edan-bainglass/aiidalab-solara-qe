import typing as t

import pydantic as pdt


class Model(pdt.BaseModel):
    model_config = pdt.ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def get_options(cls, field_name: str):
        if field_name not in cls.model_fields:
            print(f"Field '{field_name}' not found in model {cls.__name__}")
            return []
        if t.get_origin(cls.model_fields[field_name].annotation) is not t.Literal:
            print(f"Field '{field_name}' has no options")
            return []
        return t.get_args(cls.model_fields[field_name].annotation)

    def get_model_state(self) -> dict:
        return self.model_dump(exclude_none=True)
