""" CircleCI API client

This module implements the CircleCI API client, which acts as an interface between the raw
JSON responses from the CircleCI API and the dictionary abstraction provided by this library.
"""
from __future__ import annotations

import logging as _log
from functools import wraps

import requests

from circleci.exceptions import CircleCIError
from circleci.utils import validate_login
from resources import dict_to_circleci_resource

LOG = _log.getLogger("circleci")
LOG.addHandler(_log.NullHandler())


class CircleCI:
    BASE_URL = "https://circleci.com"

    def __init__(self, token: str,
                 logging: bool = True,
                 max_retries: int = 3,
                 retry_delay: int = 1,
                 timeout: None or int = None,
                 login_validation: bool = False):
        self.__token = token
        self.headers = {'Circle-Token': self.__token}

        LOG.setLevel(_log.INFO if logging else _log.CRITICAL)
        self.log = LOG

        if login_validation:
            valid, response = validate_login(self.BASE_URL, self.headers)
            if not valid:
                raise CircleCIError("Cannot logic with the provided token. "
                                    "Please check the token.",
                                    response.status_code,
                                    response=response)

        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout

    def _get(self, endpoint: str) -> requests.Response:
        """
        Perform a GET request.
        :param endpoint: API endpoint
        :return: response
        """
        response = requests.get(self.BASE_URL + endpoint,
                                headers=self.headers)
        return response

    def _post(self, endpoint: str,
              payload: dict) -> requests.Response:
        """
        Perform a POST request.
        :param endpoint: API endpoint
        :param payload: request payload
        :return: response
        """
        response = requests.post(self.BASE_URL + endpoint,
                                 headers=self.headers,
                                 json=payload)
        return response

    def _delete(self, endpoint: str) -> requests.Response:
        """
        Perform a DELETE request.
        :param endpoint: API endpoint
        :return: response
        """
        response = requests.delete(self.BASE_URL + endpoint,
                                   headers=self.headers)
        return response

    def _patch(self, endpoint: str,
               payload: dict) -> requests.Response:
        """
        Perform a PATCH request.
        :param endpoint: API endpoint
        :param payload: request payload
        :return: response
        """
        response = requests.patch(self.BASE_URL + endpoint,
                                  headers=self.headers,
                                  json=payload)
        return response

    def _put(self, endpoint: str,
             payload: dict) -> requests.Response:
        """
        Perform a PUT request.
        :param endpoint: API endpoint
        :param payload: request payload
        :return: response
        """
        response = requests.put(self.BASE_URL + endpoint,
                                headers=self.headers,
                                json=payload)
        return response

    def response_validation(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.log.info('Validating response...')
            response = func(*args, **kwargs)
            response_data = response.json()
            response_data.update(
                {'metadata': {'status_code': response.status_code, 'url': response.url}})
            if response.status_code in range(200, 299):
                self.log.info('Response validated successfully.')
                return dict_to_circleci_resource(response_data)
            self.log.error('Failed to validate response.')
            raise CircleCIError('Failed to validate response.',
                                response.status_code,
                                response=response)

        return wrapper

    # -------------------------------- Context Endpoints -------------------------------- #

    @response_validation
    def create_context(self, name: str,
                       owner_id: str,
                       owner_type: str = "organization") -> requests.Response:
        """
        Create a new context.
        :param name: context name
        :param owner_id: context description
        :param owner_type: context owner type
        :return: context dict

        Example:
        payload = "{\"name\":\"string\",\
        "owner\":{\"id\":\"497f6eca-6276-4993-bfeb-53cbbbba6f08\",
        \"type\":\"organization\"}}"

        """
        endpoint = f"/api/v2/context"
        payload = {
            "name": name,
            "owner": {
                "id": owner_id,
                "type": owner_type
            }
        }
        return self._post(endpoint, payload)

    @response_validation
    def list_contexts(self) -> requests.Response:
        """
        List all contexts for the owner.
        :return: list of contexts
        """
        endpoint = "/api/v2/context"
        return self._get(endpoint)

    @response_validation
    def delete_context(self, context_id: str) -> requests.Response:
        """
        Delete a context.
        :param context_id: context id
        :return: response
        """
        endpoint = f"/api/v2/context/{context_id}"
        return self._delete(endpoint)

    @response_validation
    def get_context(self, context_id: str) -> requests.Response:
        """
        Get a context.
        :param context_id: context id
        :return: context dict
        """
        endpoint = f"/api/v2/context/{context_id}"
        return self._get(endpoint)

    @response_validation
    def list_environment_variables_in_context(self, context_id: str,
                                              page_token: str or None = None) -> requests.Response:
        """
        List all environment variables in a context.
        :param context_id: context id
        :param page_token: page token (str)
        :return: list of environment variables
        """
        endpoint = (f"/api/v2/context/{context_id}/environment-variable"
                    f"{'?page-token=' + page_token if page_token else ''}")
        return self._get(endpoint)
