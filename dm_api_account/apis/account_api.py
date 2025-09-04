from dm_api_account.models.request.change_password import ChangePassword
from dm_api_account.models.request.registration import Registration
from dm_api_account.models.request.reset_password import ResetPassword
from dm_api_account.models.response.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.response.user_envelope import UserEnvelope

from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            registration: Registration,
            **kwargs
            ):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
            # exclude_none=True - если поле является не обязательным мы не будем его пепедавать
            # by_alias заполение модели будет идти через дополнительное слово указанное отдельно
            )
        return response

    def get_v1_account(
            self,
            validate_response=True,
            **kwargs
            ):
        """
        Get current user
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
            )
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    def put_v1_account_token(
            self,
            token,
            validate_response=True,
            **kwargs
            ):
        """
        Activate registered user
        """
        response = self.put(
            path=f'/v1/account/{token}'
            )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_email(
            self,
            registration: Registration,
            validate_response = True
            ):
        """
        PUT
        Change registered user email
        :param json_data:
        :param kwargs:
        :return:
        """
        response = self.put(
            path=f'/v1/account/email',
            json=registration.model_dump(exclude_none=True, by_alias=True)
            )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def post_v1_account_password(
            self,
            reset_password : ResetPassword,
            validate_response=True,
            **kwargs
            ):
        """
        POST
        Reset registered user password
        :param json_data
        :param kwargs:
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True)
            )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_password(
            self,
            change_password : ChangePassword,
            headers,
            validate_response = True,
            **kwargs
            ):
        """
        PUT
        Change registered user password
        :param json_data
        :param kwargs:
        :return:
        """
        pass
        response = self.put(
            path=f'/v1/account/password',
            json = change_password.model_dump(exclude_none=True, by_alias=True),
            headers=headers
            )
        if validate_response:
            return UserEnvelope(**response.json())
        return response
