""" Exceptions for the CircleCI API client. """
from __future__ import annotations

import tempfile

from requests import Response


class CircleCIError(Exception):
    """
    A general error raised for any issues encountered during the operation of the client.
    """

    def __init__(self,
                 text: str or None = None,
                 status_code: int or None = None,
                 url: str or None = None,
                 request: Response or None = None,
                 response: Response or None = None,
                 log_to_tempfile: bool = False):
        """
        Creates a CircleCIError.

        Args:
            text (str): The error message.
            status_code (int): The HTTP status code.
            url (str): The URL of the request.
            request (Response): The request object.
            response (Response): The response object.
            log_to_tempfile (bool): A flag to determine if the error should be logged to a tempfile.

        Returns:
            CircleCIError: The CircleCIError instance.
        """
        self.status_code = status_code
        self.text = text
        self.url = url
        self.request = request
        self.response = response
        self.log_to_tempfile = log_to_tempfile

    def __str__(self) -> str:
        message = f"CircleCIError HTTP {self.status_code}"
        if self.url:
            message += f" url: {self.url}"

        details = ""
        if self.request:
            if hasattr(self.request, "headers"):
                details += f"\n\trequest headers = {self.request.headers}"
            if hasattr(self.request, "text"):
                details += f"\n\trequest text = {self.request.text}"
        if self.response:
            if hasattr(self.response, "headers"):
                details += f"\n\tresponse headers = {self.response.headers}"
            if hasattr(self.response, "text"):
                details += f"\n\tresponse text = {self.response.text}"

        if self.log_to_tempfile:
            _, file_name = tempfile.mkstemp(suffix=".tmp", prefix="circlecierror-")
            with open(file_name, "w", encoding="utf-8") as f:
                message += f" details: {file_name}"
                f.write(details)
        else:
            if self.text:
                message += f"\n\ttext: {self.text}"
            message += f"\n\t{details}"

        return message
