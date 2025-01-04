""" CircleCI API client

This module implements the CircleCI API client, which acts as an interface between the raw
JSON responses from the CircleCI API and the dictionary abstraction provided by this library.
"""
from __future__ import annotations

import logging as _log
from functools import wraps

import requests
from requests import Response

from circleci.exceptions import CircleCIError
from circleci.resources import dict_to_circleci_resource, CircleCIPropertyHolder
from circleci.utils import validate_login

LOG = _log.getLogger("circleci")
LOG.addHandler(_log.NullHandler())


class CircleCI:
    """ CircleCI API client. """

    BASE_URL = "https://circleci.com"

    def __init__(self, token: str,
                 logging: bool = True,
                 max_retries: int = 3,
                 retry_delay: int = 1,
                 timeout: None or int = 3,
                 login_validation: bool = False):
        self.__token = token
        self.headers = {'Circle-Token': self.__token}

        LOG.setLevel(_log.INFO if logging else _log.CRITICAL)
        self.log = LOG

        if login_validation:
            valid, response = validate_login(self.BASE_URL, self.headers)
            if not valid:
                raise CircleCIError("Cannot login with the provided token. "
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
                                headers=self.headers,
                                timeout=self.timeout)
        return response

    def _post(self, endpoint: str,
              payload: dict or None = None) -> requests.Response:
        """
        Perform a POST request.
        :param endpoint: API endpoint
        :param payload: request payload
        :return: response
        """
        response = requests.post(self.BASE_URL + endpoint,
                                 headers=self.headers,
                                 json=payload,
                                 timeout=self.timeout)
        return response

    def _delete(self, endpoint: str) -> requests.Response:
        """
        Perform a DELETE request.
        :param endpoint: API endpoint
        :return: response
        """
        response = requests.delete(self.BASE_URL + endpoint,
                                   headers=self.headers,
                                   timeout=self.timeout)
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
                                  json=payload,
                                  timeout=self.timeout)
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
                                json=payload,
                                timeout=self.timeout)
        return response

    @staticmethod
    def response_validation(func):
        """
        Decorator to validate the response from the CircleCI API.

        Args:
            func (function): function to decorate

        Returns:
            function: decorated function
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.log.info('Validating response...')
            response = func(self, *args, **kwargs)
            response_data = response.json()
            if isinstance(response_data, dict):
                response_data.update(
                    {'metadata': {'status_code': response.status_code, 'url': response.url}})
            elif isinstance(response_data, list):
                response_data = {'response': response_data,
                                 'metadata': {'status_code': response.status_code,
                                              'url': response.url}}
            if response.status_code in range(200, 299):
                self.log.info('Response validated successfully.')
                return dict_to_circleci_resource(response_data)
            self.log.error('Failed to validate response.')
            raise CircleCIError('Failed to validate response.', response.status_code,
                                response=response)

        return wrapper

    # -------------------------------- Context Endpoints -------------------------------- #

    @response_validation
    def create_context(self, name: str,
                       owner_id: str,
                       owner_type: str = "organization") -> CircleCIPropertyHolder or Response:
        """
        Create a new context.
        :param name: context name (str)
        :param owner_id: context description (str)
        :param owner_type: context owner type (str)
        :return: context dict (json)

        Example:
        payload = "{\"name\":\"string\",\
        "owner\":{\"id\":\"497f6eca-6276-4993-bfeb-53cbbbba6f08\",
        \"type\":\"organization\"}}"

        """
        endpoint = "/api/v2/context"
        payload = {
            "name": name,
            "owner": {
                "id": owner_id,
                "type": owner_type
            }
        }
        return self._post(endpoint, payload)

    @response_validation
    def list_contexts(self) -> CircleCIPropertyHolder or Response:
        """
        List all contexts for the owner.
        :return: list of contexts
        """
        endpoint = "/api/v2/context"
        return self._get(endpoint)

    @response_validation
    def delete_context(self, context_id: str) -> CircleCIPropertyHolder or Response:
        """
        Delete a context.
        :param context_id: context id (uuid)
        :return: response (json)
        """
        endpoint = f"/api/v2/context/{context_id}"
        return self._delete(endpoint)

    @response_validation
    def get_context(self, context_id: str) -> CircleCIPropertyHolder or Response:
        """
        Get a context.
        :param context_id: context id (uuid)
        :return: context dict (json)
        """
        endpoint = f"/api/v2/context/{context_id}"
        return self._get(endpoint)

    @response_validation
    def list_environment_variables_in_context(
            self, context_id: str,
            page_token: str or None = None) -> CircleCIPropertyHolder or Response:
        """
        List all environment variables in a context.
        :param context_id: context id
        :param page_token: page token (str)
        :return: list of environment variables
        """
        endpoint = f"/api/v2/context/{context_id}/environment-variable" \
                   f"{'?page-token=' + page_token if page_token else ''}"
        return self._get(endpoint)

    @response_validation
    def remove_environment_variable_from_context(
            self, context_id: str,
            env_var_name: str) -> CircleCIPropertyHolder or Response:
        """
        Remove an environment variable from a context.
        :param context_id: context id (uuid)
        :param env_var_name: environment variable name (str)
        :return: response
        """
        endpoint = f"/api/v2/context/{context_id}/environment-variable/{env_var_name}"
        return self._delete(endpoint)

    @response_validation
    def add_or_update_env_variable(self, context_id: str,
                                   env_var_name: str,
                                   env_var_value: str) -> CircleCIPropertyHolder or Response:
        """
        Add or update an environment variable in a context.
        :param context_id: context id (uuid)
        :param env_var_name: environment variable name (str)
        :param env_var_value: environment variable value (str)
        :return: response
        """
        endpoint = f"/api/v2/context/{context_id}/environment-variable/{env_var_name}"
        payload = {
            "value": env_var_value
        }
        return self._put(endpoint, payload)

    @response_validation
    def get_context_restrictions(self, context_id: str) -> CircleCIPropertyHolder or Response:
        """
        Get the restrictions for a context.
        :param context_id: context id (uuid)
        :return: response
        """
        endpoint = f"/api/v2/context/{context_id}/restrictions"
        return self._get(endpoint)

    @response_validation
    def create_context_restriction(self, context_id: str,
                                   restriction_type: str,
                                   restriction_value: str) -> CircleCIPropertyHolder or Response:
        """
        Create a context restriction.
        :param context_id: context id (uuid)
        :param restriction_type: restriction type (str)
        :param restriction_value: restriction value (str)
        :return: response
        """
        endpoint = f"/api/v2/context/{context_id}/restrictions"
        payload = {
            "restriction_type": restriction_type,
            "restriction_value": restriction_value
        }
        return self._post(endpoint, payload)

    @response_validation
    def delete_context_restriction(self, context_id: str,
                                   restriction_id: str) -> CircleCIPropertyHolder or Response:
        """
        Delete a context restriction.
        :param context_id: context id (uuid)
        :param restriction_id: restriction id (uuid)
        :return: response
        """
        endpoint = f"/api/v2/context/{context_id}/restrictions/{restriction_id}"
        return self._delete(endpoint)

    # -------------------------------- User Endpoints -------------------------------- #

    @response_validation
    def get_current_user_information(self) -> CircleCIPropertyHolder or Response:
        """
        Get information about the user.
        :return: user information
        """
        endpoint = "/api/v2/me"
        return self._get(endpoint)

    @response_validation
    def get_user_projects(self) -> CircleCIPropertyHolder or Response:
        """
        Get all projects for the user.
        :return: user projects
        """
        endpoint = "/api/v1.1/projects"
        return self._get(endpoint)

    @response_validation
    def get_user_collaborations(self) -> CircleCIPropertyHolder or Response:
        """
        Get all collaborations for the user.
        :return: user collaborations
        """
        endpoint = "/api/v2/me/collaborations"
        return self._get(endpoint)

    @response_validation
    def get_user_information(self, user_id: str) -> CircleCIPropertyHolder or Response:
        """
        Get information about a user.
        :param user_id: user id (uuid)
        :return: user information
        """
        endpoint = f"/api/v2/user/{user_id}"
        return self._get(endpoint)

    # -------------------------------- Pipeline Endpoints -------------------------------- #

    @response_validation
    def get_list_of_pipelines_user_follow(self, org_slug: str or None = None,
                                          page_token: str or None = None,
                                          mine: bool = False) -> CircleCIPropertyHolder or Response:
        """
        Get list of pipelines user is following.
        :return: list of pipelines
        """
        params = {
            "org-slug": org_slug,
            "page-token": page_token,
            "mine": "true" if mine else None
        }
        query_string = "&".join(f"{k}={v}" for k, v in params.items() if v)
        endpoint = f"/api/v2/pipeline{'?' + query_string if query_string else ''}"
        return self._get(endpoint)

    @response_validation
    def continue_pipeline(self, continuation_key: str,
                          configuration: str,
                          parameters: dict) -> CircleCIPropertyHolder or Response:
        """
        Continue a pipeline from the setup phase.
        :param continuation_key: continuation key (str)
        :param configuration: configuration (str)
        :param parameters: parameters (dict)
        :return: response
        """
        endpoint = "/api/v2/pipeline/continue"
        payload = {
            "continuation-key": continuation_key,
            "configuration": configuration,
            "parameters": parameters
        }
        return self._post(endpoint, payload)

    @response_validation
    def get_pipeline_by_id(self, pipeline_id: str) -> CircleCIPropertyHolder or Response:
        """
        Get a pipeline by id.
        :param pipeline_id: pipeline id (uuid)
        :return: pipeline
        """
        endpoint = f"/api/v2/pipeline/{pipeline_id}"
        return self._get(endpoint)

    @response_validation
    def get_pipeline_config_by_id(self, pipeline_id: str) -> CircleCIPropertyHolder or Response:
        """
        Get the configuration for a pipeline by id.
        :param pipeline_id: pipeline id (uuid)
        :return: pipeline configuration
        """
        endpoint = f"/api/v2/pipeline/{pipeline_id}/config"
        return self._get(endpoint)

    @response_validation
    def get_pipeline_values_by_id(self, pipeline_id: str) -> CircleCIPropertyHolder or Response:
        """
        Get the values for a pipeline by id.
        :param pipeline_id: pipeline id (uuid)
        :return: pipeline values
        """
        endpoint = f"/api/v2/pipeline/{pipeline_id}/values"
        return self._get(endpoint)

    @response_validation
    def get_pipeline_workflow_by_id(
            self, pipeline_id: str,
            page_token: str or None = None) -> CircleCIPropertyHolder or Response:
        """
        Get the workflow for a pipeline by id.
        :param pipeline_id: pipeline id (uuid)
        :param page_token: page token (str)
        :return: pipeline workflow
        """
        endpoint = f"/api/v2/pipeline/{pipeline_id}/workflow" \
                   f"{'?page-token=' + page_token if page_token else ''}"
        return self._get(endpoint)

    @response_validation
    def trigger_pipeline(self, project_slug: str,
                         branch: str = None,
                         tag: str = None,
                         parameters: dict = None) -> CircleCIPropertyHolder or Response:
        """
        Trigger a pipeline.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param branch: branch (str)
        :param tag: tag (str)
        :param parameters: parameters (dict)
        :return: response
        """
        if branch and tag:
            raise CircleCIError(
                "Both `branch` and `tag` cannot be provided. Please provide only one.")

        endpoint = f"/api/v2/project/{project_slug}/pipeline"
        payload = {k: v for k, v in
                   {"branch": branch, "tag": tag, "parameters": parameters or {}}.items() if v}

        return self._post(endpoint, payload)

    @response_validation
    def get_all_pipelines_for_project(
            self, project_slug: str,
            page_token: str or None = None,
            branch: str or None = None) -> CircleCIPropertyHolder or Response:
        """
        Get all pipelines for a project.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param page_token: page token (str)
        :param branch: branch (str)
        :return: pipelines
        """
        params = {
            "branch": branch,
            "page-token": page_token,
        }
        query_string = "&".join(f"{k}={v}" for k, v in params.items() if v)
        endpoint = f"/api/v2/project/{project_slug}/pipeline" \
                   f"{'?' + query_string if query_string else ''}"
        return self._get(endpoint)

    @response_validation
    def get_pipeline_triggered_by_current_user(
            self, project_slug: str,
            page_token: str or None = None) -> CircleCIPropertyHolder or Response:
        """
        Get pipeline triggered by the current user.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param page_token: page token (str)
        :return: pipeline
        """
        endpoint = f"/api/v2/project/{project_slug}/pipeline/mine" \
                   f"{'?page-token=' + page_token if page_token else ''}"
        return self._get(endpoint)

    @response_validation
    def get_pipeline_by_number(self, project_slug: str,
                               pipeline_number: int) -> CircleCIPropertyHolder or Response:
        """
        Get a pipeline by number.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param pipeline_number: pipeline number (int)
        :return: pipeline
        """
        endpoint = f"/api/v2/project/{project_slug}/pipeline/{pipeline_number}"
        return self._get(endpoint)

    # -------------------------------- Job Endpoints -------------------------------- #

    @response_validation
    def cancel_job_by_id(self, job_id: str) -> CircleCIPropertyHolder or Response:
        """
        Cancel a job by id.
        :param job_id: job id (uuid)
        :return: response
        """
        endpoint = f"/api/v2/job/{job_id}/cancel"
        return self._post(endpoint)

    @response_validation
    def get_job_by_number(self, project_slug: str,
                          job_number: int) -> CircleCIPropertyHolder or Response:
        """
        Get a job by number.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param job_number: job number (int)
        :return: job
        """
        endpoint = f"/api/v2/project/{project_slug}/job/{job_number}"
        return self._get(endpoint)

    @response_validation
    def cancel_job_by_number(self, project_slug: str,
                             job_number: int) -> CircleCIPropertyHolder or Response:
        """
        Cancel a job by number.
        :param project_slug:
        :param job_number: job number (int)
        :return: response
        """
        endpoint = f"/api/v2/project/{project_slug}/job/{job_number}/cancel"
        return self._post(endpoint)

    @response_validation
    def get_job_artifacts(self, project_slug: str,
                          job_number: str) -> CircleCIPropertyHolder or Response:
        """
        Get job artifacts.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param job_number: job number (int)
        :return: job artifacts
        """
        endpoint = f"/api/v2/project/{project_slug}/{job_number}/artifacts"
        return self._get(endpoint)

    @response_validation
    def get_job_metadata(self, project_slug: str,
                         job_number: str) -> CircleCIPropertyHolder or Response:
        """
        Get job metadata.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param job_number: job number (int)
        :return: job metadata
        """
        endpoint = f"/api/v2/project/{project_slug}/{job_number}/tests"
        return self._get(endpoint)

    # -------------------------------- Workflow Endpoints -------------------------------- #

    @response_validation
    def get_workflow_by_id(self, workflow_id: str) -> CircleCIPropertyHolder or Response:
        """
        Get a workflow by id.
        :param workflow_id: workflow id (uuid)
        :return: workflow
        """
        endpoint = f"/api/v2/workflow/{workflow_id}"
        return self._get(endpoint)

    @response_validation
    def approve_workflow_job(self, workflow_id: str,
                             job_id: str) -> CircleCIPropertyHolder or Response:
        """
        Approve a workflow job.
        :param workflow_id: workflow id (uuid)
        :param job_id: job id (uuid)
        :return: response
        """
        endpoint = f"/api/v2/workflow/{workflow_id}/approve/{job_id}"
        return self._post(endpoint)

    @response_validation
    def cancel_workflow(self, workflow_id: str) -> CircleCIPropertyHolder or Response:
        """
        Cancel a running workflow.
        :param workflow_id: workflow id (uuid)
        :return: response
        """
        endpoint = f"/api/v2/workflow/{workflow_id}/cancel"
        return self._post(endpoint)

    @response_validation
    def get_workflow_jobs(self, workflow_id: str,
                          page_token: str or None = None) -> CircleCIPropertyHolder or Response:
        """
        Get all jobs for a workflow.
        :param workflow_id: workflow id (uuid)
        :param page_token: page token (str)
        :return: workflow jobs
        """
        endpoint = f"/api/v2/workflow/{workflow_id}/job" \
                   f"{'?page-token=' + page_token if page_token else ''}"
        return self._get(endpoint)

    @response_validation
    def rerun_workflow(self, workflow_id: str,
                       enable_ssh: bool = False,
                       from_failed: bool = False,
                       jobs: list or None = None,
                       sparse_tree: bool = False) -> CircleCIPropertyHolder or Response:
        """
        Rerun a workflow.
        :param workflow_id: workflow id (uuid)
        :param enable_ssh: enable ssh (bool)
        :param from_failed: from failed (bool)
        :param jobs: jobs (list)
        :param sparse_tree: sparse tree (bool)
        :return: response
        """
        endpoint = f"/api/v2/workflow/{workflow_id}/rerun"
        payload = {k: v for k, v in {
            "enable_ssh": enable_ssh,
            "from_failed": from_failed,
            "jobs": jobs,
            "sparse_tree": sparse_tree
        }.items() if v is not None}

        return self._post(endpoint, payload)

    # -------------------------------- Webhook Endpoints -------------------------------- #

    @response_validation
    def get_webhooks(self, scope_id: str,
                     scope_type: str) -> CircleCIPropertyHolder or Response:
        """
        Get webhooks.
        :param scope_id: scope id (uuid)
        :param scope_type: scope type (str)
        :return: webhooks
        """
        endpoint = f"/api/v2/webhook?scope-id={scope_id}&scope-type={scope_type}"
        return self._get(endpoint)

    @response_validation
    def create_outbound_webhook(self, name: str,
                                events: list,
                                url: str,
                                verify_tls: bool,
                                signing_secret: str,
                                scope: dict) -> CircleCIPropertyHolder or Response:
        """
        Create an outbound webhook.
        :param name: name (str)
        :param events: events (list)
        :param url: url (str)
        :param verify_tls: verify tls (bool)
        :param signing_secret: signing secret (str)
        :param scope: scope (dict)
        :return: response
        """
        endpoint = "/api/v2/webhook"
        payload = {
            "name": name,
            "events": events,
            "url": url,
            "verify-tls": verify_tls,
            "signing-secret": signing_secret,
            "scope": scope
        }
        return self._post(endpoint, payload)

    @response_validation
    def get_webhook_by_id(self, webhook_id: str) -> CircleCIPropertyHolder or Response:
        """
        Get a webhook by id.
        :param webhook_id: webhook id (uuid)
        :return: webhook
        """
        endpoint = f"/api/v2/webhook/{webhook_id}"
        return self._get(endpoint)

    @response_validation
    def update_webhook_by_id(self, webhook_id: str,
                             name: str,
                             events: list,
                             url: str,
                             verify_tls: bool,
                             signing_secret: str) -> CircleCIPropertyHolder or Response:
        """
        Update a webhook by id.
        :param webhook_id: webhook id (uuid)
        :param name: name (str)
        :param events: events (list)
        :param url: url (str)
        :param verify_tls: verify tls (bool)
        :param signing_secret: signing secret (str)
        :return: response
        """
        endpoint = f"/api/v2/webhook/{webhook_id}"
        payload = {
            "name": name,
            "events": events,
            "url": url,
            "verify-tls": verify_tls,
            "signing-secret": signing_secret
        }
        return self._put(endpoint, payload)

    @response_validation
    def delete_webhook_by_id(self, webhook_id: str) -> CircleCIPropertyHolder or Response:
        """
        Delete a webhook by id.
        :param webhook_id: webhook id (uuid)
        :return: response
        """
        endpoint = f"/api/v2/webhook/{webhook_id}"
        return self._delete(endpoint)

    # ------------------------- OIDC Token Management Endpoints ------------------------- #

    @response_validation
    def delete_org_level_claims(self, org_id: str,
                                claims: str) -> CircleCIPropertyHolder or Response:
        """
        Delete organization level claims.
        :param org_id: organization id (uuid)
        :param claims: comma separated list of claims to delete (str)
        :return: response
        """
        endpoint = f"/api/v2/org/{org_id}/oidc-custom-claims?claims={claims}"
        return self._delete(endpoint)

    @response_validation
    def get_org_level_claims(self, org_id: str) -> CircleCIPropertyHolder or Response:
        """
        Get organization level claims.
        :param org_id: organization id (uuid)
        :return: claims
        """
        endpoint = f"/api/v2/org/{org_id}/oidc-custom-claims"
        return self._get(endpoint)

    @response_validation
    def create_or_update_org_level_claims(self, org_id: str,
                                          audience: list,
                                          ttl: str) -> CircleCIPropertyHolder or Response:
        """
        Create or update organization level claims.
        :param org_id: organization id (uuid)
        :param audience: audience (list)
        :param ttl: ttl (str)
        :return: response
        """
        endpoint = f"/api/v2/org/{org_id}/oidc-custom-claims"
        payload = {k: v for k, v in {
            "audience": audience,
            "ttl": ttl
        }.items() if v is not None}

        return self._patch(endpoint, payload)

    @response_validation
    def delete_project_level_claims(self, org_id: str,
                                    project_id: str,
                                    claims: str) -> CircleCIPropertyHolder or Response:
        """
        Delete project level claims.
        :param org_id: organization id (uuid)
        :param project_id: project id (uuid)
        :param claims: comma separated list of claims to delete (str)
        :return: response
        """
        endpoint = f"/api/v2/org/{org_id}/project/{project_id}/oidc-custom-claims?claims={claims}"
        return self._delete(endpoint)

    @response_validation
    def get_project_level_claims(self, org_id: str,
                                 project_id: str) -> CircleCIPropertyHolder or Response:
        """
        Get project level claims.
        :param org_id: organization id (uuid)
        :param project_id: project id (uuid)
        :return: claims
        """
        endpoint = f"/api/v2/org/{org_id}/project/{project_id}/oidc-custom-claims"
        return self._get(endpoint)

    @response_validation
    def create_or_update_project_level_claims(self, org_id: str,
                                              project_id: str,
                                              audience: list,
                                              ttl: str) -> CircleCIPropertyHolder or Response:
        """
        Create or update project level claims.
        :param org_id: organization id (uuid)
        :param project_id: project id (uuid)
        :param audience: audience (list)
        :param ttl: ttl (str)
        :return: response
        """
        endpoint = f"/api/v2/org/{org_id}/project/{project_id}/oidc-custom-claims"
        payload = {k: v for k, v in {
            "audience": audience,
            "ttl": ttl
        }.items() if v is not None}

        return self._patch(endpoint, payload)

    # -------------------------------- Project Endpoints -------------------------------- #

    @response_validation
    def get_project(self, project_slug: str) -> CircleCIPropertyHolder or Response:
        """
        Get a project.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :return: project
        """
        endpoint = f"/api/v2/project/{project_slug}"
        return self._get(endpoint)

    @response_validation
    def create_checkout_key(self, project_slug: str,
                            key_type: str) -> CircleCIPropertyHolder or Response:
        """
        Create a checkout key.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param key_type: key_type (str)
        :return: response
        """
        endpoint = f"/api/v2/project/{project_slug}/checkout-key"
        payload = {
            "type": key_type
        }
        return self._post(endpoint, payload)

    @response_validation
    def get_all_checkout_keys(self, project_slug: str,
                              digest: str) -> CircleCIPropertyHolder or Response:
        """
        Get all checkout keys.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param digest: digest (str)
        :return: checkout keys
        """
        endpoint = f"/api/v2/project/{project_slug}/checkout-key" \
                   f"{'?digest=' + digest if digest else ''}"
        return self._get(endpoint)

    @response_validation
    def delete_checkout_key(self, project_slug: str,
                            fingerprint: str) -> CircleCIPropertyHolder or Response:
        """
        Delete a checkout key.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param fingerprint: fingerprint (str)
        :return: response
        """
        endpoint = f"/api/v2/project/{project_slug}/checkout-key/{fingerprint}"
        return self._delete(endpoint)

    @response_validation
    def get_checkout_key(self, project_slug: str,
                         fingerprint: str) -> CircleCIPropertyHolder or Response:
        """
        Get a checkout key.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param fingerprint: fingerprint (str)
        :return: checkout key
        """
        endpoint = f"/api/v2/project/{project_slug}/checkout-key/{fingerprint}"
        return self._get(endpoint)

    @response_validation
    def create_env_var(self, project_slug: str,
                       name: str,
                       value: str) -> CircleCIPropertyHolder or Response:
        """
        Create an environment variable.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param name: name (str)
        :param value: value (str)
        :return: response
        """
        endpoint = f"/api/v2/project/{project_slug}/envvar"
        payload = {
            "name": name,
            "value": value
        }
        return self._post(endpoint, payload)

    @response_validation
    def get_all_env_vars(self, project_slug: str) -> CircleCIPropertyHolder or Response:
        """
        Get all environment variables.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :return: environment variables
        """
        endpoint = f"/api/v2/project/{project_slug}/envvar"
        return self._get(endpoint)

    @response_validation
    def delete_env_var(self, project_slug: str,
                       name: str) -> CircleCIPropertyHolder or Response:
        """
        Delete an environment variable.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param name: name (str)
        :return: response
        """
        endpoint = f"/api/v2/project/{project_slug}/envvar/{name}"
        return self._delete(endpoint)

    @response_validation
    def get_masked_env_var(self, project_slug: str,
                           name: str) -> CircleCIPropertyHolder or Response:
        """
        Get a masked environment variable.
        :param project_slug: vcs-slug/org-name/repo-name | e.g.: gh/CircleCI-Public/api-preview-docs
        :param name: name (str)
        :return: masked environment variable
        """
        endpoint = f"/api/v2/project/{project_slug}/envvar/{name}"
        return self._get(endpoint)

    @response_validation
    def create_new_project(self, vcs_type: str,
                           org_name: str,
                           repo_name: str) -> CircleCIPropertyHolder or Response:
        """
        Create a new project.
        :param vcs_type: vcs type (str)
        :param org_name: organization name (str)
        :param repo_name: repository name (str)
        :return: response
        """
        endpoint = f"/api/v2/project/{vcs_type}/{org_name}/{repo_name}"
        return self._post(endpoint)

    @response_validation
    def get_project_setting(self, vcs_type: str,
                            org_name: str,
                            repo_name: str) -> CircleCIPropertyHolder or Response:
        """
        Returns a list of the advanced settings for a CircleCI project.
        :param vcs_type: vcs type (str)
        :param org_name: organization name (str)
        :param repo_name: repository name (str)
        :return: response
        """
        endpoint = f"/api/v2/project/{vcs_type}/{org_name}/{repo_name}/settings"
        return self._get(endpoint)

    @response_validation
    def update_project_setting(self, vcs_type: str,
                               org_name: str,
                               repo_name: str,
                               settings: dict) -> CircleCIPropertyHolder or Response:
        """
        Update the advanced settings for a CircleCI project.
        :param vcs_type: vcs type (str)
        :param org_name: organization name (str)
        :param repo_name: repository name (str)
        :param settings: settings (dict)
        :return: response
        """
        endpoint = f"/api/v2/project/{vcs_type}/{org_name}/{repo_name}/settings"
        payload = {
            "advanced": settings
        }
        return self._patch(endpoint, payload)

    # -------------------------------- Custom Methods -------------------------------- #

    def get_last_build_artifacts_by_project_name(self, project_slug: str,
                                                 branch: str) -> CircleCIPropertyHolder or Response:
        """
        Get build artifacts by project name.

        Args:
            project_slug (str): project slug
            branch (str): branch name

        Returns:
            CircleCIPropertyHolder or Response: build artifacts urls
        """
        pipeline_id = self.get_all_pipelines_for_project(project_slug,
                                                         branch=branch).items[0].id
        workflow_id = self.get_pipeline_workflow_by_id(pipeline_id).items[0].id
        job_number = self.get_workflow_jobs(workflow_id).items[0].job_number
        return self.get_job_artifacts(project_slug, job_number)
