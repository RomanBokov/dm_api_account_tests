from pprint import pprint
from  json import loads
import requests

def test_post_v1_account():
    # Регистрация пользователя
    login = 'user91'
    password = 'password'
    email = 'nazgyl-921@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account',  json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, "Пользователь не был создан"
    # Получить письмаиз почтового сервера


    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params,  verify=False)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"
    #pprint(response.json())
    # Получить активный токен
    token = None
    for item in response.json()['items']:
        user_data =loads(item['Content']['Body'])
        user_login = user_data['Login']


        if user_login == login:
            print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)

    assert token is not None, "Токен для пользователя логин не был получен"
    # Активация пользователя


    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"
    # Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"