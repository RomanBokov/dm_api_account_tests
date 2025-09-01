
def test_put_v1_account_password(account_helper,prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    #Регистрация пользователя
    token = account_helper.register_new_user(login=login, email=email, password= password)
    #Активация токена
    response = account_helper.dm_account_api.account_api.put_v1_account_token(token=token)
    #Авторизация пользователя со старым паролем
    response_auth_client = account_helper.user_login(login=login,password=password)
    token = {
        "x-dm-auth-token": response_auth_client.headers["x-dm-auth-token"]
        }
    #Смена пароля с пробросом авторизационного токена в хэдэры и указанием токена для сброса пароля из письма
    account_helper.chang_password(login=login, password=password,email=email, token_auth= token)
    #Авторизация пользователя с новым паролем
    account_helper.user_login(login=login, password=f'new{password}')
