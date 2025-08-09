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

from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi


def test_put_v1_account_email():

    # Регистрация пользователя
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')
    login = 'user90' + f'{uuid.uuid4()}'
    password = 'password'
    email =  f'{uuid.uuid4()}' +'@mail.ru'
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

    # Активация пользователя

    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
        }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"
    data = json.loads(response.text)
    registration_str = data["resource"]["registration"]
    assert "registration" in data["resource"]
    assert isinstance(registration_str, str)

    #Меняем зарегистрируемую почту пользователя
    emailnew = f"new{email}"
    json_data = {
        'login': login,
        'email': emailnew,
        'password': password,
        }
    headers = {'token': token}
    account_api.heders = headers
    response = account_api.put_v1_account_email(json_data=json_data)
    assert response.status_code == 200, "Пользыватель не активировался"
    print(response)

    # Авторизоваться повторно под старыми данными

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 403, "Пользователь не смог авторизоваться"

    # Получить письмаиз почтового сервера повторно

    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"


    # ищем на почте новый токен

    token2 = get_activation_token_by_new_email(emailnew, response)
    print(token2)
    assert token2 is not None, "Токен для пользователя логин не был получен"
    assert token != token2, "Токен не изменен"

    # Активация пользователя

    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
        }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"
    data = json.loads(response.text)
    registration_str = data["resource"]["registration"]
    assert "registration" in data["resource"]
    assert isinstance(registration_str, str)







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

def get_activation_token_by_new_email(
        emailnew,
        response
        ):
    token = []
    if 'items' not in response.json():
        return None
    for item in response.json()['items']:
        # Проверяем поле To (может быть списком получателей)
        if 'To' in item:
            for recipient in item['To']:
                search_mail = f'{recipient.get('Mailbox')}@{recipient.get('Domain')}'
                if isinstance(recipient, dict) and search_mail == emailnew:
                    # Если нашли нужного получателя, извлекаем ссылку
                    if 'Content' in item and 'Body' in item['Content']:
                        try:
                            body_data = json.loads(item['Content']['Body'])
                            if 'ConfirmationLinkUrl' in body_data:
                                token.append(
                                    {
                                        'mailbox': emailnew,
                                        'confirmation_link': body_data['ConfirmationLinkUrl'],
                                        'message_id': item.get('ID'),
                                        'created': item.get('Created')
                                        }
                                    )
                        except json.JSONDecodeError:
                            continue
    return token if token else None

