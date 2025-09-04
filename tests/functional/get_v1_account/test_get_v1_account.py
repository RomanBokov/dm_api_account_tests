import allure

from checkers.get_v1_account import GetV1Account


@allure.suite("Тесты на получение текущего пользователя GET v1/account")
@allure.sub_suite("Позитивные тесты")
class TestGetV1Account:

    @allure.title("Проверка авторизации созданного пользователя")
    def test_get_v1_account(self, auth_account_helper):
       response = auth_account_helper.dm_account_api.account_api.get_v1_account()
       GetV1Account.check_response_values_get_auth_account_helper(response=response)

    @allure.title("Проверка не авторизации созданного пользователя")
    def test_get_v1_account_no_auth(self, account_helper):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)

     #Получить информацию о пользователе (используя авторизованный клиент)
    @allure.title("Тест на получение информации о пользователе")
    def test_open_information_user(self, auth_account_helper):
        response =auth_account_helper.dm_account_api.account_api.get_v1_account()
        GetV1Account.check_response_values_get_auth_account_helper(response=response)



