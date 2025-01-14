""" CircleCI utils used internally. """

from __future__ import annotations

import requests


def validate_login(base_url: str,
                   headers: dict) -> tuple[bool, requests.Response]:
    """
    Validate the login of the user.

    Args:
        base_url (str): The base URL of the CircleCI API.
        headers (dict): The headers to use for the request.

    Returns:
        tuple[bool, requests.Response]: A tuple containing a boolean indicating if
                                        the login was successful and the response.
    """
    endpoint = '/api/v2/me'
    response = requests.get(base_url + endpoint,
                            headers=headers,
                            timeout=3)
    if response.status_code == 200:
        return True, response
    return False, response
