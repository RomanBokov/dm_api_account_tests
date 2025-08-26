import json
import time
from json import loads
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from retrying import retry


def retry_if_result_none(
        result
        ):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(
        function
        ):

    def wraper(
            *args,
            **kwargs
            ):
        token = None
        count = 0
        while token is None:
            print(f'Попытка получения токена {count}')
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено количество попыток получения активационного токена!")
            if token:
                return token
        return token
    return wraper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
            ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(
            self,
            login: str,
            password: str
            ):
        resource = self.dm_account_api.login_api.post_v1_account_login(
            json_data={
                'login': login,
                'password': password
                }
            )
        pass
        token = {
            "x-dm-auth-token": resource.headers["x-dm-auth-token"]
            }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)
        return token


    def create_new_user(
            self,
            login: str,
            password: str,
            email: str
            ):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
            }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, "Пользователь не был создан"

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
            ):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
            }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, "Пользователь не был создан"
        # Получить письмаиз почтового сервера

        # Получить активный токен
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, "Токен для пользователя логин не был получен"
        # Активация пользователя

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"
        return token

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
            ):
        # Авторизоваться

        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
            }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        registration_str = response.json()["resource"]["registration"]
        assert isinstance(registration_str, str)
        return response

    def chang_email(
            self,
            emailnew: str,
            login: str,
            password: str
            ):
        # Меняем зарегистрируемую почту пользователя

        json_data = {
            'login': login,
            'email': emailnew,
            'password': password,
            }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, "Пользыватель не активировался"

        # # Авторизоваться повторно под старыми данными
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        # ищем на почте новый токен
        token2 = self.get_activation_newtoken_by_email(emailnew, response)
        assert token2 is not None, "Токен для пользователя логин не был получен"
        # assert token != token2, "Токен не изменен"
        # Активация пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(token=token2)
        assert response.status_code == 200, "Пользователь не был активирован"


    def chang_password(self,
            email: str,
            login: str,
            password: str,
            token_auth : str
            ):
        json_data2 = {
            "login": login,
            "email": email
            }
        self.dm_account_api.account_api.post_v1_account_password(json_data=json_data2)

        token2 = self.get_activation_token_by_login(login=login,token_type="token2")
        json_data = {
            "login": login,
            "token": token2,
            "oldPassword": password,
            "newPassword": f'new{password}'
            }
        response_put_v1_account_password = self.dm_account_api.account_api.put_v1_account_password(
            json_data=json_data, headers=token_auth
            )
        assert response_put_v1_account_password.status_code == 200, "Пароль не сбросился"

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login,
            token_type: str = 'activation'
            ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                field_name = 'ConfirmationLinkUrl'
                if token_type != 'activation':
                    field_name = 'ConfirmationLinkUri'
                confirmation_link = user_data.get(field_name)
                if confirmation_link:
                    token = confirmation_link.split('/')[-1]
                    break
                if token:
                    break  # Прерываем внешний цикл

        return token

    @staticmethod
    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_newtoken_by_email(
            email,
            response
            ):
        token = []
        if not response.json().get("items"):
            return None

        for item in response.json()["items"]:
            try:
                for recipient in item["To"]:
                    search_mail = f"{recipient['Mailbox']}@{recipient['Domain']}"
                    if search_mail == email:
                        body_data = json.loads(item["Content"]["Body"])
                        token.append(
                            {
                                "mailbox": email,
                                "confirmation_link": body_data["ConfirmationLinkUrl"],
                                "message_id": item.get("ID"),
                                "created": item.get("Created"),
                                }
                            )
                        if isinstance(token, list):
                            confirmation_link = token[0]['confirmation_link']
                            tokennew = confirmation_link.split('/')[-1]
                            return tokennew
            except KeyError:
                continue

        return token

        # def activation_registration_user(self, token):
        #     header = {
        #         'token ': token
        #         }
        #     self.dm_account_api.account_api.headers = header
        # response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        # assert response.status_code == 200, "Пользователь не активирован"
        # assert 'Player' in response.json()['resource']['roles']
