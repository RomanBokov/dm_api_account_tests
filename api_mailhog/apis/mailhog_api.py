import requests


class MailhogApi:
    def __init__(
            self,
            host
            ):
        self.host = host


    def get_api_v2_messages(
            self,
            limit=50,
            **kwargs
            ):
        '''
        Get user emails
        :return:
        '''
        params = {
            'limit': limit
            }
        response = requests.get(
            url=f'{self.host}/api/v2/messages',
            params=params,
            verify=False
            )
        return response
