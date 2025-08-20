'''
Аутентификация через учетные данные

- Регистрируемся
- Получаем активационный токен
- Активируем
- Заходим
'''
import json
import random
import uuid

import pytest

from helpers.account_helper import AccountHelper
'''
- Регистрируемся

- Получаем активационный токен

- Активируем
'''
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                          sort_keys=True)
        ]
    )
@pytest.fixture
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client

@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')
    account = DMApiAccount(configuration=dm_api_configuration)
    return account
@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog= mailhog_api)
    return account_helper


def test_post_v1_account(account_helper):
    # Регистрация пользователя
    uuid_new = uuid.uuid4()
    login = 'user90' + f'{uuid_new}'
    password = 'password'
    email = f'{uuid_new}' + '@mail.ru'
    account_helper.register_new_user(login=login, password= password, email= email)
    account_helper.user_login(login=login, password=password)