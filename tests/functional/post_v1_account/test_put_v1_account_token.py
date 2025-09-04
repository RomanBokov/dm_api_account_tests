
import allure


@allure.suite("Тесты вктивации зарегистированного пользователя PUT v1/account/token")
@allure.sub_suite("Позитивные тесты")
class TestPutV1AccountToken:

    @allure.title("Активация зарегистрированного пользователя")
    def test_put_v1_account_token(self, account_helper, prepare_user):

        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        # актирировать зарегистрированного пользователя
        account_helper.register_new_user(login=login, password=password, email=email)
