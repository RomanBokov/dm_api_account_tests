import time


def test_post_v1_account_exit(auth_account_helper):
    # a = auth_account_helper.auth_client

    resource = auth_account_helper.auth_client(login='user90f2abcc9e-2d7a-4bd0-b607-275fd71385e4',password='password')
    resource_close= auth_account_helper.dm_account_api.login_api.delete_v1_account_login_all(headers=resource)
    assert resource_close.status_code == 204 , "Пользователь не был авторизован"