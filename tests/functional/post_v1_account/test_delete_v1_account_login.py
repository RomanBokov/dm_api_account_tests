
def test_post_v1_account_exit(auth_account_helper):
    #Валер auth_account_helper.dm_account_api.account_api. подчеркивается с предупреждением Fixture '
    # auth_account_helper.dm_account_api.account_api' is not requested by test functions or @pytest.mark.usefixtures
    # marker
    # Причем так во всем проекте
    resource = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
    token = {
        "x-dm-auth-token": resource.headers["x-dm-auth-token"]
        }
    auth_account_helper.dm_account_api.login_api.delete_v1_account_login(token)