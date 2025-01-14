"""The root of the CircleCI package namespace."""

from __future__ import annotations

try:
    import importlib.metadata

    __version__ = importlib.metadata.version("circleci-api-python")
except (ImportError, Exception):
    __version__ = "unknown"

from circleci_api_python.client import CircleCI
from circleci_api_python.exceptions import CircleCIError

__all__ = (
    "__version__",
    "CircleCI",
    "CircleCIError",
)
