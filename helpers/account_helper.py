import json
import time
from json import loads

from dm_api_account.models.Request.change_password import ChangePassword
from dm_api_account.models.Request.login_credentials import LoginCredentials
from dm_api_account.models.Request.registration import Registration
from dm_api_account.models.Request.reset_password import ResetPassword
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
        resource = self.user_login(
            login=login,
            password=password
            )
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
        registration = Registration(
            login=login,
            password=password,
            email=email
            )
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не был создан {response.json()}"
        token = self.get_activation_token_by_login(login=login)
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response


    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
            ):
        registration = Registration(
            login=login,
            email=email,
            password=password
            )

        self.dm_account_api.account_api.post_v1_account(registration=registration)

        # Получить письмаиз почтового сервера

        # Получить активный токен
        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, "Время активации превышено"
        assert token is not None, "Токен для пользователя логин не был получен"
        # Активация пользователя

        self.dm_account_api.account_api.put_v1_account_token(token=token)
        #assert response.status_code == 200, "Пользователь не был активирован"
        return token

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response=False,
            validate_headers=False
            ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me = remember_me
            )
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
            )
        if validate_headers:
            assert response.headers['x-dm-auth-token'], "Токен для пользователя не был получен"
            assert response.status_code == 200, "Пользователь не смог авторизироваться"
        return response

    def chang_email(
            self,
            emailnew: str,
            login: str,
            password: str
            ):
        # Меняем зарегистрируемую почту пользователя

        registration = Registration(
            login=login,
            email=emailnew,
            password=password
            )
        self.dm_account_api.account_api.put_v1_account_email(registration=registration)


        # # Авторизоваться повторно под старыми данными
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        # ищем на почте новый токен
        token2 = self.get_activation_newtoken_by_email(emailnew, response)
        assert token2 is not None, "Токен для пользователя логин не был получен"
        # assert token != token2, "Токен не изменен"
        # Активация пользователя
        self.dm_account_api.account_api.put_v1_account_token(token=token2)


    def chang_password(
            self,
            email: str,
            login: str,
            password: str,
            token_auth: str
            ):
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)

        token2 = self.get_activation_token_by_login(login=login, token_type="token2")
        change_password = ChangePassword(
            login = login,
            token= token2,
            oldPassword = password,
            newPassword =f'new{password}'
        )
        self.dm_account_api.account_api.put_v1_account_password(
            change_password=change_password, headers=token_auth
            )

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
