from checkers.post_v1_account import PostV1Account


### для словаря используется has_key . a для объекта has_property, starts_with - проверяем начало по регулярке
### all_of - выполнение всех проверок


def test_post_v1_account(
        account_helper,
        prepare_user
        ):
    # Регистрация пользователя
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.create_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    PostV1Account.check_response_values(response)





