from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    )


class ResetPassword(BaseModel):
    model_config = ConfigDict(extra="forbid") # Обязательныли поля , нужно нам это заполнять для сиреализации
    login: str = Field(..., description="Login")
    email : str = Field(..., description="Email")