
def test_put_v1_account_email(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    emailnew = f"new{prepare_user.email}"

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    # Меняем зарегистрируемую почту пользователя
    account_helper.chang_email(emailnew=emailnew, login=login, password= password)
    # Авторизоваться
    account_helper.user_login(login=login, password=password)
