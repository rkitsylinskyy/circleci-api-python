""" CircleCI utils used internally. """

from __future__ import annotations

import requests


def validate_login(base_url: str,
                   headers: dict) -> tuple[bool, requests.Response]:
    """
    Validate the login of the user.
    :param base_url: base url of the CircleCI API
    :param headers: authentication headers
    :return: bool
    """
    endpoint = '/api/v2/me'
    response = requests.get(base_url + endpoint,
                            headers=headers)
    if response.status_code == 200:
        return True, response
    return False, response
