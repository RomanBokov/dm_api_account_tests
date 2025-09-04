import json
from functools import wraps

import allure
import curlify


def allure_attach(
        func
        ):
    @wraps(func)
    def wrapper(
            *args,
            **kwargs
            ):
        body = kwargs.get("json") or kwargs.get("data")
        response = func(*args, **kwargs)
        try:
            if hasattr(response, 'request'):
                curl = curlify.to_curl(response.request)
                allure.attach(curl, name="curl", attachment_type=allure.attachment_type.TEXT)
        except:
            pass

        if body:
            allure.attach(
                json.dumps(body, indent=4),
                name="request_body",
                attachment_type=allure.attachment_type.JSON,
                )

        try:
            if hasattr(response, 'json'):
                response_json = response.json()
                allure.attach(
                    json.dumps(response_json, indent=4),
                    name="response_body",
                    attachment_type=allure.attachment_type.JSON,
                    )
        except json.JSONDecodeError:
            if hasattr(response, 'text'):
                response_text = response.text
                allure.attach(
                    response_text if response_text else f"Status: {response.status_code}",
                    name="response_body",
                    attachment_type=allure.attachment_type.TEXT
                    )

        return response

    return wrapper