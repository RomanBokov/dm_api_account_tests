'''
- Регистрируемся

- Получаем активационный токен

- Активируем
'''
import random
import time
from datetime import datetime
import uuid
from json import loads

from helpers import account_helper
from helpers.account_helper import AccountHelper
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                          sort_keys=True)
        ]
    )




def test_put_v1_account_token():

    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)
    login = 'user90' + f'{uuid.uuid4()}'
    password = 'password'
    email = f'{uuid.uuid4()}' + '@mail.ru'
    response_new_user, token_new_user =account_helper.register_new_user(login=login, password=password, email=email)
    #актирировать зарегистрированного пользователя
    account_helper.activation_registration_user(token=token_new_user)