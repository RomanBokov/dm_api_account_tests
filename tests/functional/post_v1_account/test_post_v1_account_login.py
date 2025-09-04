import allure


@allure.suite("Тесты на аутентификацию пользователя POST v1/account/login")
@allure.sub_suite("Позитивные тесты")
class TestPostV1AccountLogin:

    @allure.title("Аутентификация с помощью учетных данных")
    def test_post_v1_account(self, account_helper, prepare_user):
        login = prepare_user.login
        password  = prepare_user.password
        email = prepare_user.email
        account_helper.register_new_user(login=login, password= password, email= email)
        account_helper.user_login(login=login, password=password)