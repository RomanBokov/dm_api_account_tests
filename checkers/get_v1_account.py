from datetime import datetime

from assertpy import soft_assertions, assert_that as assert_that_assertpy
from hamcrest import (
    assert_that,
    all_of,
    has_property,
    has_properties,
    starts_with,
    contains_inanyorder,
    has_item,
    equal_to,
    )

from dm_api_account.models.Response.user_envelope import UserRole


class GetV1Account():

    @classmethod
    def check_response_values_get_auth_account_helper(cls, response):
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
        with soft_assertions():
            assert_that_assertpy(response.resource.login).is_equal_to("user90f2abcc9e-2d7a-4bd0-b607-275fd71385e4")
            print("Прошла проверка логина")
            assert_that_assertpy(response.resource.registration).is_instance_of(datetime)
            print("Прошла проверка даты")
            assert_that_assertpy(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)
            print("Прошла проверка ролей пользователя")
    @classmethod
    def check_open_information_user(cls, response):
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
