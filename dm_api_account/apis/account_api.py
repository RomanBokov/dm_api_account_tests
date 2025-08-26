import requests

from main import headers
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            json_data,
            **kwargs
            ):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=json_data
            )
        return response

    def get_v1_account(
            self,
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
        return response

    def put_v1_account_token(
            self,
            token,
            **kwargs
            ):
        """
        Activate registered user
        """
        response = self.put(
            path=f'/v1/account/{token}'
            )
        return response

    def put_v1_account_email(
            self,
            json_data
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
            json=json_data
            )
        return response

    def post_v1_account_password(
            self,
            json_data,
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
            json=json_data
            )
        return response

    def put_v1_account_password(
            self,
            json_data,
            headers,
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
            json = json_data,
            headers=headers
            )
        return response
