import unittest
from unittest.mock import patch, Mock

from circleci.client import CircleCI, CircleCIError


class TestCircleCIClient(unittest.TestCase):

    @patch('requests.post')
    def test_create_context_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "test_context",
                                           "owner": {"id": "owner_id", "type": "organization"}}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.create_context("test_context", "owner_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"name": "test_context",
                                             "owner": {"id": "owner_id", "type": "organization"}})

    @patch('requests.post')
    def test_create_context_invalid_owner(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid owner"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_context("test_context", "invalid_owner")

    @patch('requests.post')
    def test_create_context_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_context("test_context", "owner_id")

    @patch('requests.get')
    def test_list_contexts_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "context_id", "name": "context_name"}]
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.list_contexts()

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {'response': [{'id': 'context_id', 'name': 'context_name'}]})

    @patch('requests.get')
    def test_list_contexts_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not Found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.list_contexts()

    @patch('requests.get')
    def test_list_contexts_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.list_contexts()

    @patch('requests.delete')
    def test_delete_context_successful(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Context deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_context("context_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Context deleted successfully"})

    @patch('requests.delete')
    def test_delete_context_not_found(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_context("invalid_context_id")

    @patch('requests.delete')
    def test_delete_context_server_error(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_context("context_id")

    @patch('requests.get')
    def test_get_context_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "context_id", "name": "context_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_context("context_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "context_id", "name": "context_name"})

    @patch('requests.get')
    def test_get_context_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_context("invalid_context_id")

    @patch('requests.get')
    def test_get_context_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_context("context_id")

    @patch('requests.get')
    def test_list_environment_variables_in_context_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"name": "ENV_VAR", "value": "value"}]
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.list_environment_variables_in_context("context_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {'response': [{'name': 'ENV_VAR', 'value': 'value'}]})

    @patch('requests.get')
    def test_list_environment_variables_in_context_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.list_environment_variables_in_context("invalid_context_id")

    @patch('requests.get')
    def test_list_environment_variables_in_context_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.list_environment_variables_in_context("context_id")

    @patch('requests.delete')
    def test_remove_environment_variable_from_context_successful(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Environment variable removed successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.remove_environment_variable_from_context("context_id", "env_var_name")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {"message": "Environment variable removed successfully"})

    @patch('requests.delete')
    def test_remove_environment_variable_from_context_not_found(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context or environment variable not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.remove_environment_variable_from_context("invalid_context_id", "env_var_name")

    @patch('requests.delete')
    def test_remove_environment_variable_from_context_server_error(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.remove_environment_variable_from_context("context_id", "env_var_name")

    @patch('requests.put')
    def test_add_or_update_env_variable_successful(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": "Environment variable added/updated successfully"}
        mock_put.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.add_or_update_env_variable("context_id", "env_var_name", "env_var_value")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {"message": "Environment variable added/updated successfully"})

    @patch('requests.put')
    def test_add_or_update_env_variable_not_found(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context not found"}
        mock_put.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.add_or_update_env_variable("invalid_context_id", "env_var_name", "env_var_value")

    @patch('requests.put')
    def test_add_or_update_env_variable_server_error(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_put.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.add_or_update_env_variable("context_id", "env_var_name", "env_var_value")

    @patch('requests.get')
    def test_get_context_restrictions_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"restrictions": ["restriction1", "restriction2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_context_restrictions("context_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"restrictions": ["restriction1", "restriction2"]})

    @patch('requests.get')
    def test_get_context_restrictions_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_context_restrictions("invalid_context_id")

    @patch('requests.get')
    def test_get_context_restrictions_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_context_restrictions("context_id")

    @patch('requests.post')
    def test_create_context_restriction_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Restriction created successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.create_context_restriction("context_id", "restriction_type",
                                                     "restriction_value")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Restriction created successfully"})

    @patch('requests.post')
    def test_create_context_restriction_invalid_context(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_context_restriction("invalid_context_id", "restriction_type",
                                              "restriction_value")

    @patch('requests.post')
    def test_create_context_restriction_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_context_restriction("context_id", "restriction_type", "restriction_value")

    @patch('requests.delete')
    def test_delete_context_restriction_successful(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Restriction deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_context_restriction("context_id", "restriction_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Restriction deleted successfully"})

    @patch('requests.delete')
    def test_delete_context_restriction_not_found(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context or restriction not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_context_restriction("invalid_context_id", "restriction_id")

    @patch('requests.delete')
    def test_delete_context_restriction_server_error(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_context_restriction("context_id", "restriction_id")

    @patch('requests.get')
    def test_get_current_user_information_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "user_id", "name": "user_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_current_user_information()

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "user_id", "name": "user_name"})

    @patch('requests.get')
    def test_get_current_user_information_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "User not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_current_user_information()

    @patch('requests.get')
    def test_get_current_user_information_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_current_user_information()

    @patch('requests.get')
    def test_get_user_projects_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "project_id", "name": "project_name"}]
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_user_projects()

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {'response': [{'id': 'project_id', 'name': 'project_name'}]})

    @patch('requests.get')
    def test_get_user_projects_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Projects not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_user_projects()

    @patch('requests.get')
    def test_get_user_projects_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_user_projects()

    @patch('requests.get')
    def test_get_user_collaborations_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "collab_id", "name": "collab_name"}]
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_user_collaborations()

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {'response': [{'id': 'collab_id', 'name': 'collab_name'}]})

    @patch('requests.get')
    def test_get_user_collaborations_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Collaborations not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_user_collaborations()

    @patch('requests.get')
    def test_get_user_collaborations_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_user_collaborations()

    @patch('requests.get')
    def test_get_user_information_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "user_id", "name": "user_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_user_information("user_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "user_id", "name": "user_name"})

    @patch('requests.get')
    def test_get_user_information_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "User not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_user_information("invalid_user_id")

    @patch('requests.get')
    def test_get_user_information_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_user_information("user_id")

    @patch('requests.get')
    def test_get_list_of_pipelines_user_follow_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"pipelines": ["pipeline1", "pipeline2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_list_of_pipelines_user_follow(org_slug="org_slug")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"pipelines": ["pipeline1", "pipeline2"]})

    @patch('requests.get')
    def test_get_list_of_pipelines_user_follow_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipelines not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_list_of_pipelines_user_follow(org_slug="invalid_org_slug")

    @patch('requests.get')
    def test_get_list_of_pipelines_user_follow_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_list_of_pipelines_user_follow(org_slug="org_slug")

    @patch('requests.post')
    def test_continue_pipeline_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Pipeline continued successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.continue_pipeline("continuation_key", "configuration", {"param": "value"})

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Pipeline continued successfully"})

    @patch('requests.post')
    def test_continue_pipeline_invalid_key(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid continuation key"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.continue_pipeline("invalid_key", "configuration", {"param": "value"})

    @patch('requests.post')
    def test_continue_pipeline_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.continue_pipeline("continuation_key", "configuration", {"param": "value"})

    @patch('requests.get')
    def test_get_pipeline_by_id_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "pipeline_id", "name": "pipeline_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_pipeline_by_id("pipeline_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "pipeline_id", "name": "pipeline_name"})

    @patch('requests.get')
    def test_get_pipeline_by_id_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipeline not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_by_id("invalid_pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_by_id_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_by_id("pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_config_by_id_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"config": "pipeline_config"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_pipeline_config_by_id("pipeline_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"config": "pipeline_config"})

    @patch('requests.get')
    def test_get_pipeline_config_by_id_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipeline config not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_config_by_id("invalid_pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_config_by_id_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_config_by_id("pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_values_by_id_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"values": "pipeline_values"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_pipeline_values_by_id("pipeline_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"values": "pipeline_values"})

    @patch('requests.get')
    def test_get_pipeline_values_by_id_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipeline values not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_values_by_id("invalid_pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_values_by_id_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_values_by_id("pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_workflow_by_id_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"workflow": "workflow_data"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_pipeline_workflow_by_id("pipeline_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"workflow": "workflow_data"})

    @patch('requests.get')
    def test_get_pipeline_workflow_by_id_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Workflow not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_workflow_by_id("invalid_pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_workflow_by_id_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_workflow_by_id("pipeline_id")

    @patch('requests.post')
    def test_trigger_pipeline_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Pipeline triggered successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.trigger_pipeline("gh/CircleCI-Public/api-preview-docs", branch="main")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Pipeline triggered successfully"})

    @patch('requests.post')
    def test_trigger_pipeline_invalid_branch_and_tag(self, mock_post):
        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.trigger_pipeline("gh/CircleCI-Public/api-preview-docs", branch="main",
                                    tag="v1.0")

    @patch('requests.post')
    def test_trigger_pipeline_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.trigger_pipeline("gh/CircleCI-Public/api-preview-docs", branch="main")

    @patch('requests.get')
    def test_get_all_pipelines_for_project_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"pipelines": ["pipeline1", "pipeline2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_all_pipelines_for_project("gh/CircleCI-Public/api-preview-docs")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"pipelines": ["pipeline1", "pipeline2"]})

    @patch('requests.get')
    def test_get_all_pipelines_for_project_with_branch(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"pipelines": ["pipeline1"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_all_pipelines_for_project("gh/CircleCI-Public/api-preview-docs",
                                                        branch="main")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"pipelines": ["pipeline1"]})

    @patch('requests.get')
    def test_get_all_pipelines_for_project_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipelines not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_all_pipelines_for_project("invalid_project_slug")

    @patch('requests.get')
    def test_get_all_pipelines_for_project_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_all_pipelines_for_project("gh/CircleCI-Public/api-preview-docs")

    @patch('requests.get')
    def test_get_pipeline_triggered_by_current_user_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"pipelines": ["pipeline1", "pipeline2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_pipeline_triggered_by_current_user(
            "gh/CircleCI-Public/api-preview-docs")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"pipelines": ["pipeline1", "pipeline2"]})

    @patch('requests.get')
    def test_get_pipeline_triggered_by_current_user_with_page_token(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"pipelines": ["pipeline1"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_pipeline_triggered_by_current_user(
            "gh/CircleCI-Public/api-preview-docs", page_token="token")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"pipelines": ["pipeline1"]})

    @patch('requests.get')
    def test_get_pipeline_triggered_by_current_user_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipelines not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_triggered_by_current_user("invalid_project_slug")

    @patch('requests.get')
    def test_get_pipeline_triggered_by_current_user_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_triggered_by_current_user("gh/CircleCI-Public/api-preview-docs")

    @patch('requests.get')
    def test_get_pipeline_by_number_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "pipeline_id", "name": "pipeline_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_pipeline_by_number("gh/CircleCI-Public/api-preview-docs", 1)

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "pipeline_id", "name": "pipeline_name"})

    @patch('requests.get')
    def test_get_pipeline_by_number_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipeline not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_by_number("gh/CircleCI-Public/api-preview-docs", 999)

    @patch('requests.get')
    def test_get_pipeline_by_number_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_by_number("gh/CircleCI-Public/api-preview-docs", 1)

    @patch('requests.post')
    def test_cancel_job_by_id_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Job cancelled successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.cancel_job_by_id("job_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Job cancelled successfully"})

    @patch('requests.post')
    def test_cancel_job_by_id_not_found(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Job not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.cancel_job_by_id("invalid_job_id")

    @patch('requests.post')
    def test_cancel_job_by_id_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.cancel_job_by_id("job_id")

    @patch('requests.get')
    def test_get_job_by_number_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "job_id", "name": "job_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_job_by_number("gh/CircleCI-Public/api-preview-docs", 1)

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "job_id", "name": "job_name"})

    @patch('requests.get')
    def test_get_job_by_number_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Job not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_job_by_number("gh/CircleCI-Public/api-preview-docs", 999)

    @patch('requests.get')
    def test_get_job_by_number_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_job_by_number("gh/CircleCI-Public/api-preview-docs", 1)

    @patch('requests.post')
    def test_cancel_job_by_number_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Job cancelled successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.cancel_job_by_number("gh/CircleCI-Public/api-preview-docs", 1)

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Job cancelled successfully"})

    @patch('requests.post')
    def test_cancel_job_by_number_not_found(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Job not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.cancel_job_by_number("gh/CircleCI-Public/api-preview-docs", 999)

    @patch('requests.post')
    def test_cancel_job_by_number_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.cancel_job_by_number("gh/CircleCI-Public/api-preview-docs", 1)

    @patch('requests.get')
    def test_get_job_artifacts_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"path": "artifact_path", "url": "artifact_url"}]
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_job_artifacts("gh/CircleCI-Public/api-preview-docs", "1")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {'response': [{'path': 'artifact_path', 'url': 'artifact_url'}]})

    @patch('requests.get')
    def test_get_job_artifacts_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Artifacts not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_job_artifacts("gh/CircleCI-Public/api-preview-docs", "999")

    @patch('requests.get')
    def test_get_job_artifacts_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_job_artifacts("gh/CircleCI-Public/api-preview-docs", "1")

    @patch('requests.get')
    def test_get_job_metadata_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"tests": ["test1", "test2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_job_metadata("gh/CircleCI-Public/api-preview-docs", "1")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"tests": ["test1", "test2"]})

    @patch('requests.get')
    def test_get_job_metadata_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Job metadata not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_job_metadata("gh/CircleCI-Public/api-preview-docs", "999")

    @patch('requests.get')
    def test_get_job_metadata_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_job_metadata("gh/CircleCI-Public/api-preview-docs", "1")

    @patch('requests.get')
    def test_get_workflow_by_id_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "workflow_id", "name": "workflow_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_workflow_by_id("workflow_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "workflow_id", "name": "workflow_name"})

    @patch('requests.get')
    def test_get_workflow_by_id_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Workflow not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_workflow_by_id("invalid_workflow_id")

    @patch('requests.get')
    def test_get_workflow_by_id_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_workflow_by_id("workflow_id")

    @patch('requests.post')
    def test_approve_workflow_job_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Job approved successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.approve_workflow_job("workflow_id", "job_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Job approved successfully"})

    @patch('requests.post')
    def test_approve_workflow_job_not_found(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Workflow or job not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.approve_workflow_job("invalid_workflow_id", "invalid_job_id")

    @patch('requests.post')
    def test_approve_workflow_job_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.approve_workflow_job("workflow_id", "job_id")

    @patch('requests.post')
    def test_cancel_workflow_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Workflow cancelled successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.cancel_workflow("workflow_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Workflow cancelled successfully"})

    @patch('requests.post')
    def test_cancel_workflow_not_found(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Workflow not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.cancel_workflow("invalid_workflow_id")

    @patch('requests.post')
    def test_cancel_workflow_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.cancel_workflow("workflow_id")

    @patch('requests.get')
    def test_get_all_jobs_for_workflow_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jobs": ["job1", "job2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_workflow_jobs("workflow_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"jobs": ["job1", "job2"]})

    @patch('requests.get')
    def test_get_all_jobs_for_workflow_with_page_token(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jobs": ["job1"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_workflow_jobs("workflow_id", page_token="token")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"jobs": ["job1"]})

    @patch('requests.get')
    def test_get_all_jobs_for_workflow_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Workflow not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_workflow_jobs("invalid_workflow_id")

    @patch('requests.get')
    def test_get_all_jobs_for_workflow_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_workflow_jobs("workflow_id")

    @patch('requests.post')
    def test_rerun_workflow_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Workflow rerun successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.rerun_workflow("workflow_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Workflow rerun successfully"})

    @patch('requests.post')
    def test_rerun_workflow_with_ssh(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Workflow rerun with SSH successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.rerun_workflow("workflow_id", enable_ssh=True)

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Workflow rerun with SSH successfully"})

    @patch('requests.post')
    def test_rerun_workflow_from_failed(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Workflow rerun from failed successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.rerun_workflow("workflow_id", from_failed=True)

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Workflow rerun from failed successfully"})

    @patch('requests.post')
    def test_rerun_workflow_with_jobs(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": "Workflow rerun with specific jobs successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.rerun_workflow("workflow_id", jobs=["job1", "job2"])

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {"message": "Workflow rerun with specific jobs successfully"})

    @patch('requests.post')
    def test_rerun_workflow_not_found(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Workflow not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.rerun_workflow("invalid_workflow_id")

    @patch('requests.post')
    def test_rerun_workflow_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.rerun_workflow("workflow_id")
