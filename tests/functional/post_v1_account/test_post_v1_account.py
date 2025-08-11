import uuid
from  json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                          sort_keys=True)
        ]
    )

def test_post_v1_account():
    # Регистрация пользователя
    account_api = AccountApi(host='http://5.63.153.31:5051' )
    login_api = LoginApi(host='http://5.63.153.31:5051' )
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025' )
    login = 'user90' + f'{uuid.uuid4()}'
    password = 'password'
    email = f'{uuid.uuid4()}' + '@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, "Пользователь не был создан"






