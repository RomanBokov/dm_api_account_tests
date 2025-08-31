from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    )


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid") # Обязательныли поля , нужно нам это заполнять для сиреализации
    login: str = Field(..., description='User login', alias='login')
    token: str = Field(..., description='Password reset token', alias= 'token')
    old_password: str = Field(..., description='Old password', alias= 'oldPassword')
    new_password: str = Field(..., description='New password', alias= 'newPassword')