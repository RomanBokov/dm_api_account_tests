from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    )


class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra="forbid") # Обязательныли поля , нужно ли нам это заполнять для сиреализации
    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")
    remember_me : bool = Field(..., description="Запомнить меня", serialization_alias="rememberMe")
