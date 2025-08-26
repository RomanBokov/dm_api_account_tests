
def test_post_v1_account_exit(auth_account_helper):

    resource = auth_account_helper.dm_account_api.account_api.get_v1_account()
    token = {
        "x-dm-auth-token": resource.headers["x-dm-auth-token"]
        }
    resource_close= auth_account_helper.dm_account_api.login_api.delete_v1_account_login(token)
    assert resource_close.status_code == 204 , "Пользователь не был авторизован"