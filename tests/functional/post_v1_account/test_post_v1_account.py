import uuid
from helpers.account_helper import AccountHelper
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

def test_post_v1_account(account_helper):
    # Регистрация пользователя
    uuid_new = uuid.uuid4()
    login = 'user90' + f'{uuid_new}'
    password = 'password'
    email = f'{uuid_new}' + '@mail.ru'
    account_helper.create_new_user(login=login, password=password, email=email)






