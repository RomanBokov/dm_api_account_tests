from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    )


class Registration(BaseModel):
    model_config = ConfigDict(extra="forbid") # Обязательныли поля , нужно нам это заполнять для сиреализации
    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")
    email : str = Field(..., description="Email")
