import uuid

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

    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051')

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)
    uuid_new = uuid.uuid4()
    login = 'user90' + f'{uuid_new}'
    password = 'password'
    email = f'{uuid_new}' + '@mail.ru'
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    # Меняем зарегистрируемую почту пользователя
    emailnew = f"new{email}"
    account_helper.chang_email(emailnew=emailnew, login=login, password= password)
    # Авторизоваться
    account_helper.user_login(login=login, password=password)
