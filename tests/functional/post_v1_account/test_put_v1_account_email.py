'''
изменить зарегистрированную почту пользователя

 - Регистрируемся

- Получаем активационный токен

- Активируем

- Заходим

- Меняем емейл
'''
import json
import uuid
from json import loads

from helpers.account_helper import AccountHelper
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
            )
        ]
    )


def test_put_v1_account_email():

    # Регистрация пользователя
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'user90' + f'{uuid.uuid4()}'
    password = 'password'
    email = f'{uuid.uuid4()}' + '@mail.ru'
    response_new_user, token_new_user = account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)

    # Меняем зарегистрируемую почту пользователя
    emailnew = f"new{email}"

    account_helper.chang_email(emailnew=emailnew, login=login, password= password, token= token_new_user  )


    # Авторизоваться
    account_helper.user_login(login=login, password=password)
