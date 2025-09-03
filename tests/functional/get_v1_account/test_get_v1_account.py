from checkers.get_v1_account import GetV1Account


def test_get_v1_account(auth_account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    GetV1Account.check_response_values_get_auth_account_helper(response=response)




def test_get_v1_account_no_auth(account_helper):
    account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)

# Получить информацию о пользователе (используя авторизованный клиент)
def test_open_information_user(auth_account_helper):
    response =auth_account_helper.dm_account_api.account_api.get_v1_account()
    GetV1Account.check_response_values_get_auth_account_helper(response=response)



