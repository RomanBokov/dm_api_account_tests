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

from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
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
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')
    login = 'User90' + f'{random.randint(1, 999)}'
    password = 'password1'
    email = f'Mail{random.randint(1, 999)}' + '@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
        }

    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, "Пользователь не был создан"
    # Получить письмаиз почтового сервера

    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"
    # pprint(response.json())
    # Получить активный токен
    token = get_activation_token_by_login(login, response)
    print(token)
    assert token is not None, "Токен для пользователя логин не был получен"

    #актирировать зарегистрированного пользователя
    header = {'token ': token}
    account_api.headers = header
    response = account_api.put_v1_account_token(token)
    print(response.json())
    assert response.status_code == 200, "Пользователь не активирован"
    assert 'Player' in response.json()['resource']['roles']


def get_activation_token_by_login(
        login,
        response
        ):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token