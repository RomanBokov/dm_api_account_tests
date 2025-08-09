import requests

from main import headers


class AccountApi:
    def __init__(
            self,
            host,
            headers=None
            ):
        self.host = host
        self.headers = headers

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
        response = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data
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
        response = requests.put(f'{self.host}/v1/account/{token}')
        return response

    def put_v1_account_email(self,
                             json_data):
        """
        PUT
        Change registered user email
        :param json_data:
        :param kwargs:
        :return:
        """
        response = requests.put(
            url=f'{self.host}/v1/account/email',
            json=json_data,headers=self.headers
            )
        return  response