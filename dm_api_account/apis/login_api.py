import allure

from dm_api_account.models.Request.login_credentials import LoginCredentials
from dm_api_account.models.Response.user_envelope import UserEnvelope
from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(
            self,
            login_credentials: LoginCredentials,
            validate_response=True
    ):
        """Authenticate via credentials"""
        response = self.post(
            path='/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Выход из системы текущего пользователя")
    def delete_v1_account_login(
            self,
            headers,
            # validate_response=True,
            **kwargs
            ):
        response = self.delete(
            path=f'/v1/account/login',
            headers= headers,
            **kwargs
            )
        # if validate_response:
        #     return GeneralError(**response.json())
        return response

    @allure.step("Разлогирование всех пользователей")
    def delete_v1_account_login_all(
            self,
            headers,
            # validate_response=True,
            **kwargs
            ):
        response = self.delete(
            path=f'/v1/account/login/all',
            headers= headers,

            **kwargs
            )
        # if validate_response:
        #     return GeneralError(**response.json())
        return response
