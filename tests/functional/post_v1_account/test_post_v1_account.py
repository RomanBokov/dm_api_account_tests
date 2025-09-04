import uuid
import pytest

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account



def gen_random_string(length):
    return str(uuid.uuid4()).replace('-', '')[:length]

@pytest.mark.parametrize("login, password, email, expected_status, expected_message", [
    (f"{gen_random_string(2)}", "password", f'user90' + f'{gen_random_string(10)}' + "@mail.ru", 200, ""),  # короткий логин
    (f'user90' + f'{gen_random_string(10)}',gen_random_string(2), f'user90' + f'{gen_random_string(10)}' + "@mail.ru", 400,"Validation failed"),  # короткий пароль
    ("valid_login", "validPass123", "invalid-email", 400, "Validation failed"),  # невалидный email
    ("", "password", "valid@email.com", 400, "Validation failed"),  # пустой логин
    (f'user90' + f'{gen_random_string(10)}', "", f'user90' + f'{gen_random_string(10)}' + "@mail.ru", 400, "Validation failed"),  # пустой пароль
    (f'user90' + f'{gen_random_string(10)}', "password", "", 400, "Validation failed")  # пустой email
])
def test_post_v1_account(
        account_helper,
        login, password, email, expected_status, expected_message
        ):
    # Регистрация пользователя

    login = login
    password = password
    email = email
    with check_status_code_http(expected_status_code=expected_status, expected_message=expected_message):
        account_helper.create_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password, validate_response=True)
        PostV1Account.check_response_values(response)






