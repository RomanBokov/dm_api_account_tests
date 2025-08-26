
def test_get_v1_account(auth_account_helper):
    auth_account_helper.dm_account_api.account_api.get_v1_account()

def test_get_v1_account_no_auth(account_helper):
    account_helper.dm_account_api.account_api.get_v1_account()

# Получить информацию о пользователе (используя авторизованный клиент)
def test_open_information_user(auth_account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 200, "Получить информацию о пользователях не удалось"


