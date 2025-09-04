from datetime import datetime
from hamcrest import (
    assert_that,
    all_of,
    has_property,
    has_properties,
    contains_inanyorder,
    starts_with,
    equal_to,
    has_item,
    )
from checkers.http_checkers import check_status_code_http
from dm_api_account.models.response.user_envelope import UserRole


def test_get_v1_account(auth_account_helper):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account()
        assert_that(
            response, all_of(
                has_property('resource', has_property('login', starts_with('user90'))),
                has_property(
                    'resource', has_properties(
                        {
                            "roles": contains_inanyorder(UserRole.GUEST, UserRole.PLAYER)
                            }
                        )
                    ),
                # Проверка что роли содержат ожидаемые строковые значения
                has_property(
                    'resource', has_property(
                        'roles',
                        has_item(has_property('value', 'Guest'))
                        )
                    ),
                has_property(
                    'resource', has_property(
                        'roles',
                        has_item(has_property('value', 'Player'))
                        )
                    )
                )
            )

def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, "User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)



# Получить информацию о пользователе (используя авторизованный клиент)
def test_open_information_user(auth_account_helper):
    response =auth_account_helper.dm_account_api.account_api.get_v1_account()
    assert_that(
        response, all_of(
            has_property('resource', has_property('login', starts_with('user90'))),
            has_property(
                'resource', all_of(
                    has_property('login', starts_with('user90')),
                    has_property('roles', contains_inanyorder(UserRole.GUEST, UserRole.PLAYER)),
                    has_property('info', equal_to('')),
                    has_property(
                        'rating', has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                                }
                            )
                        ),
                    has_property(
                        'settings', has_properties(
                            {
                                "color_schema": equal_to('Modern'),
                                "paging": has_properties(
                                    {
                                        "posts_per_page": equal_to(10),
                                        "comments_per_page": equal_to(10),
                                        "topics_per_page": equal_to(10),
                                        "messages_per_page": equal_to(10),
                                        "entities_per_page": equal_to(10)
                                        }
                                    )
                                }
                            )
                        )
                    )
                )
            )
        )




