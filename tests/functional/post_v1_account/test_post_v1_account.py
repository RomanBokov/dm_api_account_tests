import time


def test_post_v1_account(account_helper, prepare_user):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    a= account_helper.create_new_user(login=login, password=password, email=email)
    print(a)
    resource = account_helper.user_login(login=login, password=password,validate_response=True)

    print(resource)




