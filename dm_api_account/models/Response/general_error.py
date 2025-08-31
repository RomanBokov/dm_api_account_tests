from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    )


class GeneralError(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message : str