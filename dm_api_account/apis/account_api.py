import requests


class AccountApi:
    def __init__(
            self,
            host,
            heders=None
            ):
        self.host = host
        self.heders = heders

    def post_v1_account(
            self,
            json_data
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
            token
            ):
        """
        Activate registered user
        """
        response = requests.put(f'{self.host}/v1/account/{token}')
        return response
