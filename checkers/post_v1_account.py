from datetime import datetime

import allure
from assertpy import assert_that
from hamcrest import (
    all_of,
    has_property,
    has_properties,
    equal_to,
    instance_of,
    starts_with,
    )


class PostV1Account:

    @classmethod
    @allure.step("Проверка ответа")
    def check_response_values(cls, response):
        today = datetime.now().strftime('%Y-%m-%d')
        assert_that(str(response.resource.registration), starts_with(today))
        assert_that(
            response, all_of(
                has_property('resource', has_property('login', starts_with('user90'))),
                has_property('resource', has_property('registration', instance_of(datetime))),
                has_property(
                    'resource', has_properties(
                        {
                            "rating": has_properties(
                                {
                                    "enabled": equal_to(True),
                                    "quality": equal_to(0),
                                    "quantity": equal_to(0)
                                    }
                                )
                            }
                        )
                    )
                )
            )