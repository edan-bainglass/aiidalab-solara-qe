import pydantic as pdt


class WorkflowInput(pdt.BaseModel):
    label: str
    description: str
    structure_pk: int
    parameters: dict
