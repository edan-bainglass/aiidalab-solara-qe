from pydantic import BaseModel, ConfigDict


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
