import requests

def test_post_v1_account():
    # Регистрация пользователя
    login = 'user90'
    password = 'password'
    email = 'nazgyl-92@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account',  json=json_data)
    print(response.status_code)
    print(response.text)
    # Получить письмаиз почтового сервера


    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params,  verify=False)
    print(response.status_code)
    print(response.text)
    # Получить активный токен
    ...
    # Активация пользователя


    response = requests.put('http://5.63.153.31:5051/v1/account/7aee0663-70d4-4e05-9a91-a992922f5ccf')
    print(response.status_code)
    print(response.text)
    # Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)