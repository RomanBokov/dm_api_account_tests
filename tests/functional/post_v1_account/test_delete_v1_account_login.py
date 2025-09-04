import allure


@allure.suite("Тесты на выход из системы текущего пользователя DELETE v1/account/login")
@allure.sub_suite("Позитивные тесты")
class TestDeleteV1AccountLogin:

    @allure.title("Проверка выхода из системы текущего пользователя ")
    def test_post_v1_account_exit(self, auth_account_helper):

        resource = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
        token = {
            "x-dm-auth-token": resource.headers["x-dm-auth-token"]
            }
        auth_account_helper.dm_account_api.login_api.delete_v1_account_login(token)