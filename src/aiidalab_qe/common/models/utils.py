import pydantic as pdt


class ConfiguredBaseModel(pdt.BaseModel):
    model_config = pdt.ConfigDict(arbitrary_types_allowed=True)
