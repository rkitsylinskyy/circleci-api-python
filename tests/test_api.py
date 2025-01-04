""" Tests for the CircleCI client. """
import unittest
from unittest.mock import patch, Mock

from circleci.client import CircleCI, CircleCIError


class TestCircleCIClient(unittest.TestCase):
    """ Tests for the CircleCI client. """

    @patch('requests.post')
    def test_create_context_successful(self, mock_post: Mock) -> None:
        """
        Test create context successful

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
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
    def test_create_context_invalid_owner(self, mock_post: Mock) -> None:
        """
        Test create context with invalid owner

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid owner"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_context("test_context", "invalid_owner")

    @patch('requests.post')
    def test_create_context_server_error(self, mock_post: Mock) -> None:
        """
        Test create context with server error

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_context("test_context", "owner_id")

    @patch('requests.get')
    def test_list_contexts_successful(self, mock_get: Mock) -> None:
        """
        Test list contexts successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
    def test_list_contexts_not_found(self, mock_get: Mock) -> None:
        """
        Test list contexts not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not Found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.list_contexts()

    @patch('requests.get')
    def test_list_contexts_server_error(self, mock_get: Mock) -> None:
        """
        Test list contexts with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.list_contexts()

    @patch('requests.delete')
    def test_delete_context_successful(self, mock_delete: Mock) -> None:
        """
        Test delete context successful

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Context deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_context("context_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Context deleted successfully"})

    @patch('requests.delete')
    def test_delete_context_not_found(self, mock_delete: Mock) -> None:
        """
        Test delete context not found

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_context("invalid_context_id")

    @patch('requests.delete')
    def test_delete_context_server_error(self, mock_delete: Mock) -> None:
        """
        Test delete context with server error

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_context("context_id")

    @patch('requests.get')
    def test_get_context_successful(self, mock_get: Mock) -> None:
        """
        Test get context successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "context_id", "name": "context_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_context("context_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "context_id", "name": "context_name"})

    @patch('requests.get')
    def test_get_context_not_found(self, mock_get: Mock) -> None:
        """
        Test get context not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_context("invalid_context_id")

    @patch('requests.get')
    def test_get_context_server_error(self, mock_get: Mock) -> None:
        """
        Test get context with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_context("context_id")

    @patch('requests.get')
    def test_list_environment_variables_in_context_successful(self, mock_get: Mock) -> None:
        """
        Test list environment variables in context successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"name": "ENV_VAR", "value": "value"}]
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.list_environment_variables_in_context("context_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {'response': [{'name': 'ENV_VAR', 'value': 'value'}]})

    @patch('requests.get')
    def test_list_environment_variables_in_context_not_found(self, mock_get: Mock) -> None:
        """
        Test list environment variables in context not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.list_environment_variables_in_context("invalid_context_id")

    @patch('requests.get')
    def test_list_environment_variables_in_context_server_error(self, mock_get: Mock) -> None:
        """
        Test list environment variables in context with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.list_environment_variables_in_context("context_id")

    @patch('requests.delete')
    def test_remove_environment_variable_from_context_successful(self, mock_delete: Mock) -> None:
        """
        Test remove environment variable from context successful

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Environment variable removed successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.remove_environment_variable_from_context("context_id",
                                                                   "env_var_name")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {"message": "Environment variable removed successfully"})

    @patch('requests.delete')
    def test_remove_environment_variable_from_context_not_found(self, mock_delete: Mock) -> None:
        """
        Test remove environment variable from context not found

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context or environment variable not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.remove_environment_variable_from_context("invalid_context_id",
                                                            "env_var_name")

    @patch('requests.delete')
    def test_remove_environment_variable_from_context_server_error(self, mock_delete: Mock) -> None:
        """
        Test remove environment variable from context with server error

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.remove_environment_variable_from_context("context_id",
                                                            "env_var_name")

    @patch('requests.put')
    def test_add_or_update_env_variable_successful(self, mock_put: Mock) -> None:
        """
        Test add or update environment variable successful

        Args:
            mock_put (Mock): Mock object for requests.put

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": "Environment variable added/updated successfully"}
        mock_put.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.add_or_update_env_variable("context_id",
                                                     "env_var_name",
                                                     "env_var_value")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {"message": "Environment variable added/updated successfully"})

    @patch('requests.put')
    def test_add_or_update_env_variable_not_found(self, mock_put: Mock) -> None:
        """
        Test add or update environment variable not found

        Args:
            mock_put (Mock): Mock object for requests.put

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context not found"}
        mock_put.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.add_or_update_env_variable("invalid_context_id",
                                              "env_var_name",
                                              "env_var_value")

    @patch('requests.put')
    def test_add_or_update_env_variable_server_error(self, mock_put: Mock) -> None:
        """
        Test add or update environment variable with server error

        Args:
            mock_put (Mock): Mock object for requests.put

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_put.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.add_or_update_env_variable("context_id",
                                              "env_var_name",
                                              "env_var_value")

    @patch('requests.get')
    def test_get_context_restrictions_successful(self, mock_get: Mock) -> None:
        """
        Test get context restrictions successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"restrictions": ["restriction1", "restriction2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_context_restrictions("context_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"restrictions": ["restriction1", "restriction2"]})

    @patch('requests.get')
    def test_get_context_restrictions_not_found(self, mock_get: Mock) -> None:
        """
        Test get context restrictions not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_context_restrictions("invalid_context_id")

    @patch('requests.get')
    def test_get_context_restrictions_server_error(self, mock_get: Mock) -> None:
        """
        Test get context restrictions with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_context_restrictions("context_id")

    @patch('requests.post')
    def test_create_context_restriction_successful(self, mock_post: Mock) -> None:
        """
        Test create context restriction successful

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Restriction created successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.create_context_restriction("context_id",
                                                     "restriction_type",
                                                     "restriction_value")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Restriction created successfully"})

    @patch('requests.post')
    def test_create_context_restriction_invalid_context(self, mock_post: Mock) -> None:
        """
        Test create context restriction with invalid context

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_context_restriction("invalid_context_id",
                                              "restriction_type",
                                              "restriction_value")

    @patch('requests.post')
    def test_create_context_restriction_server_error(self, mock_post: Mock) -> None:
        """
        Test create context restriction with server error

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_context_restriction("context_id",
                                              "restriction_type",
                                              "restriction_value")

    @patch('requests.delete')
    def test_delete_context_restriction_successful(self, mock_delete: Mock) -> None:
        """
        Test delete context restriction successful

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Restriction deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_context_restriction("context_id",
                                                     "restriction_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Restriction deleted successfully"})

    @patch('requests.delete')
    def test_delete_context_restriction_not_found(self, mock_delete: Mock) -> None:
        """
        Test delete context restriction not found

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Context or restriction not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_context_restriction("invalid_context_id",
                                              "restriction_id")

    @patch('requests.delete')
    def test_delete_context_restriction_server_error(self, mock_delete: Mock) -> None:
        """
        Test delete context restriction with server error

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_context_restriction("context_id", "restriction_id")

    @patch('requests.get')
    def test_get_current_user_information_successful(self, mock_get: Mock) -> None:
        """
        Test get current user information successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "user_id", "name": "user_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_current_user_information()

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "user_id", "name": "user_name"})

    @patch('requests.get')
    def test_get_current_user_information_not_found(self, mock_get: Mock) -> None:
        """
        Test get current user information not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "User not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_current_user_information()

    @patch('requests.get')
    def test_get_current_user_information_server_error(self, mock_get: Mock) -> None:
        """
        Test get current user information with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_current_user_information()

    @patch('requests.get')
    def test_get_user_projects_successful(self, mock_get: Mock) -> None:
        """
        Test get user projects successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
    def test_get_user_projects_not_found(self, mock_get: Mock) -> None:
        """
        Test get user projects not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Projects not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_user_projects()

    @patch('requests.get')
    def test_get_user_projects_server_error(self, mock_get: Mock) -> None:
        """
        Test get user projects with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_user_projects()

    @patch('requests.get')
    def test_get_user_collaborations_successful(self, mock_get: Mock) -> None:
        """
        Test get user collaborations successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
    def test_get_user_collaborations_not_found(self, mock_get: Mock) -> None:
        """
        Test get user collaborations not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Collaborations not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_user_collaborations()

    @patch('requests.get')
    def test_get_user_collaborations_server_error(self, mock_get: Mock) -> None:
        """
        Test get user collaborations with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_user_collaborations()

    @patch('requests.get')
    def test_get_user_information_successful(self, mock_get: Mock) -> None:
        """
        Test get user information successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "user_id", "name": "user_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_user_information("user_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "user_id", "name": "user_name"})

    @patch('requests.get')
    def test_get_user_information_not_found(self, mock_get: Mock) -> None:
        """
        Test get user information not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "User not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_user_information("invalid_user_id")

    @patch('requests.get')
    def test_get_user_information_server_error(self, mock_get: Mock) -> None:
        """
        Test get user information with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_user_information("user_id")

    @patch('requests.get')
    def test_get_list_of_pipelines_user_follow_successful(self, mock_get: Mock) -> None:
        """
        Test get list of pipelines user follow successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"pipelines": ["pipeline1", "pipeline2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_list_of_pipelines_user_follow(org_slug="org_slug")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"pipelines": ["pipeline1", "pipeline2"]})

    @patch('requests.get')
    def test_get_list_of_pipelines_user_follow_not_found(self, mock_get: Mock) -> None:
        """
        Test get list of pipelines user follow not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipelines not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_list_of_pipelines_user_follow(org_slug="invalid_org_slug")

    @patch('requests.get')
    def test_get_list_of_pipelines_user_follow_server_error(self, mock_get: Mock) -> None:
        """
        Test get list of pipelines user follow with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_list_of_pipelines_user_follow(org_slug="org_slug")

    @patch('requests.post')
    def test_continue_pipeline_successful(self, mock_post: Mock) -> None:
        """
        Test continue pipeline successful

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Pipeline continued successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.continue_pipeline("continuation_key",
                                            "configuration",
                                            {"param": "value"})

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Pipeline continued successfully"})

    @patch('requests.post')
    def test_continue_pipeline_invalid_key(self, mock_post: Mock) -> None:
        """
        Test continue pipeline with invalid key

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid continuation key"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.continue_pipeline("invalid_key",
                                     "configuration",
                                     {"param": "value"})

    @patch('requests.post')
    def test_continue_pipeline_server_error(self, mock_post: Mock) -> None:
        """
        Test continue pipeline with server error

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.continue_pipeline("continuation_key",
                                     "configuration",
                                     {"param": "value"})

    @patch('requests.get')
    def test_get_pipeline_by_id_successful(self, mock_get: Mock) -> None:
        """
        Test get pipeline by id successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "pipeline_id", "name": "pipeline_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_pipeline_by_id("pipeline_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "pipeline_id", "name": "pipeline_name"})

    @patch('requests.get')
    def test_get_pipeline_by_id_not_found(self, mock_get: Mock) -> None:
        """
        Test get pipeline by id not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipeline not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_by_id("invalid_pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_by_id_server_error(self, mock_get: Mock) -> None:
        """
        Test get pipeline by id with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_by_id("pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_config_by_id_successful(self, mock_get: Mock) -> None:
        """
        Test get pipeline config by id successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"config": "pipeline_config"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_pipeline_config_by_id("pipeline_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"config": "pipeline_config"})

    @patch('requests.get')
    def test_get_pipeline_config_by_id_not_found(self, mock_get: Mock) -> None:
        """
        Test get pipeline config by id not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipeline config not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_config_by_id("invalid_pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_config_by_id_server_error(self, mock_get: Mock) -> None:
        """
        Test get pipeline config by id with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_config_by_id("pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_values_by_id_successful(self, mock_get: Mock) -> None:
        """
        Test get pipeline values by id successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"values": "pipeline_values"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_pipeline_values_by_id("pipeline_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"values": "pipeline_values"})

    @patch('requests.get')
    def test_get_pipeline_values_by_id_not_found(self, mock_get: Mock) -> None:
        """
        Test get pipeline values by id not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipeline values not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_values_by_id("invalid_pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_values_by_id_server_error(self, mock_get: Mock) -> None:
        """
        Test get pipeline values by id with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_values_by_id("pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_workflow_by_id_successful(self, mock_get: Mock) -> None:
        """
        Test get pipeline workflow by id successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"workflow": "workflow_data"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_pipeline_workflow_by_id("pipeline_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"workflow": "workflow_data"})

    @patch('requests.get')
    def test_get_pipeline_workflow_by_id_not_found(self, mock_get: Mock) -> None:
        """
        Test get pipeline workflow by id not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Workflow not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_workflow_by_id("invalid_pipeline_id")

    @patch('requests.get')
    def test_get_pipeline_workflow_by_id_server_error(self, mock_get: Mock) -> None:
        """
        Test get pipeline workflow by id with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_workflow_by_id("pipeline_id")

    @patch('requests.post')
    def test_trigger_pipeline_successful(self, mock_post: Mock) -> None:
        """
        Test trigger pipeline successful

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Pipeline triggered successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.trigger_pipeline("gh/CircleCI-Public/api-preview-docs", branch="main")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Pipeline triggered successfully"})

    @patch('requests.post')
    def test_trigger_pipeline_invalid_branch_and_tag(self) -> None:
        """
        Test trigger pipeline with invalid branch and tag

        Returns:
            None
        """
        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.trigger_pipeline("gh/CircleCI-Public/api-preview-docs", branch="main",
                                    tag="v1.0")

    @patch('requests.post')
    def test_trigger_pipeline_server_error(self, mock_post: Mock) -> None:
        """
        Test trigger pipeline with server error

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.trigger_pipeline("gh/CircleCI-Public/api-preview-docs", branch="main")

    @patch('requests.get')
    def test_get_all_pipelines_for_project_successful(self, mock_get: Mock) -> None:
        """
        Test get all pipelines for project successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"pipelines": ["pipeline1", "pipeline2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_all_pipelines_for_project("gh/CircleCI-Public/api-preview-docs")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"pipelines": ["pipeline1", "pipeline2"]})

    @patch('requests.get')
    def test_get_all_pipelines_for_project_with_branch(self, mock_get: Mock) -> None:
        """
        Test get all pipelines for project with branch

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
    def test_get_all_pipelines_for_project_not_found(self, mock_get: Mock) -> None:
        """
        Test get all pipelines for project not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipelines not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_all_pipelines_for_project("invalid_project_slug")

    @patch('requests.get')
    def test_get_all_pipelines_for_project_server_error(self, mock_get: Mock) -> None:
        """
        Test get all pipelines for project with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_all_pipelines_for_project("gh/CircleCI-Public/api-preview-docs")

    @patch('requests.get')
    def test_get_pipeline_triggered_by_current_user_successful(self, mock_get: Mock) -> None:
        """
        Test get pipeline triggered by current user successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
    def test_get_pipeline_triggered_by_current_user_with_page_token(self, mock_get: Mock) -> None:
        """
        Test get pipeline triggered by current user with page token

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
    def test_get_pipeline_triggered_by_current_user_not_found(self, mock_get: Mock) -> None:
        """
        Test get pipeline triggered by current user not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipelines not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_triggered_by_current_user("invalid_project_slug")

    @patch('requests.get')
    def test_get_pipeline_triggered_by_current_user_server_error(self, mock_get: Mock) -> None:
        """
        Test get pipeline triggered by current user with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_triggered_by_current_user("gh/CircleCI-Public/api-preview-docs")

    @patch('requests.get')
    def test_get_pipeline_by_number_successful(self, mock_get: Mock) -> None:
        """
        Test get pipeline by number successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "pipeline_id", "name": "pipeline_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_pipeline_by_number("gh/CircleCI-Public/api-preview-docs", 1)

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "pipeline_id", "name": "pipeline_name"})

    @patch('requests.get')
    def test_get_pipeline_by_number_not_found(self, mock_get: Mock) -> None:
        """
        Test get pipeline by number not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Pipeline not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_by_number("gh/CircleCI-Public/api-preview-docs", 999)

    @patch('requests.get')
    def test_get_pipeline_by_number_server_error(self, mock_get: Mock) -> None:
        """
        Test get pipeline by number with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_pipeline_by_number("gh/CircleCI-Public/api-preview-docs", 1)

    @patch('requests.post')
    def test_cancel_job_by_id_successful(self, mock_post: Mock) -> None:
        """
        Test cancel job by id successful

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Job cancelled successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.cancel_job_by_id("job_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Job cancelled successfully"})

    @patch('requests.post')
    def test_cancel_job_by_id_not_found(self, mock_post: Mock) -> None:
        """
        Test cancel job by id not found

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Job not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.cancel_job_by_id("invalid_job_id")

    @patch('requests.post')
    def test_cancel_job_by_id_server_error(self, mock_post: Mock) -> None:
        """
        Test cancel job by id with server error

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.cancel_job_by_id("job_id")

    @patch('requests.get')
    def test_get_job_by_number_successful(self, mock_get: Mock) -> None:
        """
        Test get job by number successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "job_id", "name": "job_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_job_by_number("gh/CircleCI-Public/api-preview-docs", 1)

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "job_id", "name": "job_name"})

    @patch('requests.get')
    def test_get_job_by_number_not_found(self, mock_get: Mock) -> None:
        """
        Test get job by number not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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

    @patch('requests.get')
    def test_get_webhooks_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"webhooks": ["webhook1", "webhook2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_webhooks("scope_id", "scope_type")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"webhooks": ["webhook1", "webhook2"]})

    @patch('requests.get')
    def test_get_webhooks_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Webhooks not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_webhooks("invalid_scope_id", "scope_type")

    @patch('requests.get')
    def test_get_webhooks_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_webhooks("scope_id", "scope_type")

    @patch('requests.post')
    def test_create_outbound_webhook_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Webhook created successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.create_outbound_webhook(
            name="webhook_name",
            events=["event1", "event2"],
            url="https://example.com/webhook",
            verify_tls=True,
            signing_secret="secret",
            scope={"type": "project", "id": "project_id"}
        )

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Webhook created successfully"})

    @patch('requests.post')
    def test_create_outbound_webhook_invalid_scope(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid scope"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_outbound_webhook(
                name="webhook_name",
                events=["event1", "event2"],
                url="https://example.com/webhook",
                verify_tls=True,
                signing_secret="secret",
                scope={"type": "invalid_type", "id": "project_id"}
            )

    @patch('requests.post')
    def test_create_outbound_webhook_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_outbound_webhook(
                name="webhook_name",
                events=["event1", "event2"],
                url="https://example.com/webhook",
                verify_tls=True,
                signing_secret="secret",
                scope={"type": "project", "id": "project_id"}
            )

    @patch('requests.get')
    def test_get_webhook_by_id_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "webhook_id", "name": "webhook_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_webhook_by_id("webhook_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "webhook_id", "name": "webhook_name"})

    @patch('requests.get')
    def test_get_webhook_by_id_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Webhook not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_webhook_by_id("webhook_id")

    @patch('requests.get')
    def test_get_webhook_by_id_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_webhook_by_id("webhook_id")

    @patch('requests.put')
    def test_update_webhook_by_id_successful(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Webhook updated successfully"}
        mock_put.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.update_webhook_by_id(
            webhook_id="webhook_id",
            name="new_name",
            events=["event1", "event2"],
            url="https://example.com/webhook",
            verify_tls=True,
            signing_secret="new_secret"
        )

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Webhook updated successfully"})

    @patch('requests.put')
    def test_update_webhook_by_id_not_found(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Webhook not found"}
        mock_put.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.update_webhook_by_id(
                webhook_id="webhook_id",
                name="new_name",
                events=["event1", "event2"],
                url="https://example.com/webhook",
                verify_tls=True,
                signing_secret="new_secret"
            )

    @patch('requests.put')
    def test_update_webhook_by_id_server_error(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_put.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.update_webhook_by_id(
                webhook_id="webhook_id",
                name="new_name",
                events=["event1", "event2"],
                url="https://example.com/webhook",
                verify_tls=True,
                signing_secret="new_secret"
            )

    @patch('requests.delete')
    def test_delete_webhook_by_id_successful(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Webhook deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_webhook_by_id("webhook_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Webhook deleted successfully"})

    @patch('requests.delete')
    def test_delete_webhook_by_id_not_found(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Webhook not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_webhook_by_id("webhook_id")

    @patch('requests.delete')
    def test_delete_webhook_by_id_server_error(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_webhook_by_id("webhook_id")

    @patch('requests.delete')
    def test_delete_org_level_claims_successful(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Claims deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_org_level_claims("org_id", "claim1,claim2")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Claims deleted successfully"})

    @patch('requests.delete')
    def test_delete_org_level_claims_not_found(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Organization not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_org_level_claims("org_id", "claim1,claim2")

    @patch('requests.delete')
    def test_delete_org_level_claims_server_error(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_org_level_claims("org_id", "claim1,claim2")

    @patch('requests.get')
    def test_get_org_level_claims_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"claims": ["claim1", "claim2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_org_level_claims("org_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"claims": ["claim1", "claim2"]})

    @patch('requests.get')
    def test_get_org_level_claims_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Organization not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_org_level_claims("org_id")

    @patch('requests.get')
    def test_get_org_level_claims_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_org_level_claims("org_id")

    @patch('requests.patch')
    def test_create_or_update_org_level_claims_successful(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Claims created or updated successfully"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.create_or_update_org_level_claims("org_id", ["audience1", "audience2"],
                                                            "3600")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Claims created or updated successfully"})

    @patch('requests.patch')
    def test_create_or_update_org_level_claims_invalid_org(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid organization"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_or_update_org_level_claims("invalid_org_id", ["audience1", "audience2"],
                                                     "3600")

    @patch('requests.patch')
    def test_create_or_update_org_level_claims_server_error(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_or_update_org_level_claims("org_id", ["audience1", "audience2"], "3600")

    @patch('requests.delete')
    def test_delete_project_level_claims_successful(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Claims deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_project_level_claims("org_id", "project_id", "claim1,claim2")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Claims deleted successfully"})

    @patch('requests.delete')
    def test_delete_project_level_claims_not_found(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Organization or project not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_project_level_claims("org_id", "project_id", "claim1,claim2")

    @patch('requests.delete')
    def test_delete_project_level_claims_server_error(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_project_level_claims("org_id", "project_id", "claim1,claim2")

    @patch('requests.get')
    def test_get_project_level_claims_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"claims": ["claim1", "claim2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_project_level_claims("org_id", "project_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"claims": ["claim1", "claim2"]})

    @patch('requests.get')
    def test_get_project_level_claims_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_project_level_claims("org_id", "project_id")

    @patch('requests.get')
    def test_get_project_level_claims_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_project_level_claims("org_id", "project_id")

    @patch('requests.patch')
    def test_create_or_update_project_level_claims_successful(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Claims created or updated successfully"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.create_or_update_project_level_claims("org_id", "project_id",
                                                                ["audience1", "audience2"], "3600")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Claims created or updated successfully"})

    @patch('requests.patch')
    def test_create_or_update_project_level_claims_invalid_org(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid organization"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_or_update_project_level_claims("invalid_org_id", "project_id",
                                                         ["audience1", "audience2"], "3600")

    @patch('requests.patch')
    def test_create_or_update_project_level_claims_server_error(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_or_update_project_level_claims("org_id", "project_id",
                                                         ["audience1", "audience2"], "3600")

    @patch('requests.get')
    def test_get_project_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "project_id", "name": "project_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_project("gh/CircleCI-Public/api-preview-docs")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "project_id", "name": "project_name"})

    @patch('requests.get')
    def test_get_project_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_project("gh/CircleCI-Public/nonexistent-project")

    @patch('requests.get')
    def test_get_project_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_project("gh/CircleCI-Public/api-preview-docs")

    @patch('requests.post')
    def test_create_checkout_key_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Checkout key created successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.create_checkout_key("gh/CircleCI-Public/api-preview-docs", "deploy-key")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Checkout key created successfully"})

    @patch('requests.post')
    def test_create_checkout_key_invalid_project(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_checkout_key("gh/CircleCI-Public/nonexistent-project", "deploy-key")

    @patch('requests.post')
    def test_create_checkout_key_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_checkout_key("gh/CircleCI-Public/api-preview-docs", "deploy-key")

    @patch('requests.get')
    def test_get_all_checkout_keys_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"fingerprint": "fingerprint1", "type": "deploy-key"}]
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_all_checkout_keys("gh/CircleCI-Public/api-preview-docs", "")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {'response': [{'fingerprint': 'fingerprint1', 'type': 'deploy-key'}]})

    @patch('requests.get')
    def test_get_all_checkout_keys_with_digest(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"fingerprint": "fingerprint1", "type": "deploy-key"}]
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_all_checkout_keys("gh/CircleCI-Public/api-preview-docs",
                                                "digest_value")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {'response': [{'fingerprint': 'fingerprint1', 'type': 'deploy-key'}]})

    @patch('requests.get')
    def test_get_all_checkout_keys_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_all_checkout_keys("gh/CircleCI-Public/nonexistent-project", "")

    @patch('requests.get')
    def test_get_all_checkout_keys_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_all_checkout_keys("gh/CircleCI-Public/api-preview-docs", "")

    @patch('requests.delete')
    def test_delete_checkout_key_successful(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Checkout key deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_checkout_key("gh/CircleCI-Public/api-preview-docs", "fingerprint")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Checkout key deleted successfully"})

    @patch('requests.delete')
    def test_delete_checkout_key_not_found(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Checkout key not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_checkout_key("gh/CircleCI-Public/api-preview-docs",
                                       "nonexistent-fingerprint")

    @patch('requests.delete')
    def test_delete_checkout_key_server_error(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_checkout_key("gh/CircleCI-Public/api-preview-docs", "fingerprint")

    @patch('requests.get')
    def test_get_checkout_key_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"fingerprint": "fingerprint1", "type": "deploy-key"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_checkout_key("gh/CircleCI-Public/api-preview-docs", "fingerprint1")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"fingerprint": "fingerprint1", "type": "deploy-key"})

    @patch('requests.get')
    def test_get_checkout_key_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Checkout key not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_checkout_key("gh/CircleCI-Public/api-preview-docs",
                                    "nonexistent-fingerprint")

    @patch('requests.get')
    def test_get_checkout_key_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_checkout_key("gh/CircleCI-Public/api-preview-docs", "fingerprint1")

    @patch('requests.post')
    def test_create_env_var_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Environment variable created successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.create_env_var("gh/CircleCI-Public/api-preview-docs", "ENV_VAR", "value")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {"message": "Environment variable created successfully"})

    @patch('requests.post')
    def test_create_env_var_invalid_project(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_env_var("gh/CircleCI-Public/invalid-project", "ENV_VAR", "value")

    @patch('requests.post')
    def test_create_env_var_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_env_var("gh/CircleCI-Public/api-preview-docs", "ENV_VAR", "value")

    @patch('requests.get')
    def test_get_all_env_vars_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"name": "ENV_VAR", "value": "value"}]
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_all_env_vars("gh/CircleCI-Public/api-preview-docs")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {'response': [{'name': 'ENV_VAR', 'value': 'value'}]})

    @patch('requests.get')
    def test_get_all_env_vars_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_all_env_vars("gh/CircleCI-Public/api-preview-docs")

    @patch('requests.get')
    def test_get_all_env_vars_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_all_env_vars("gh/CircleCI-Public/api-preview-docs")

    @patch('requests.delete')
    def test_delete_env_var_successful(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Environment variable deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_env_var("gh/CircleCI-Public/api-preview-docs", "ENV_VAR")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {"message": "Environment variable deleted successfully"})

    @patch('requests.delete')
    def test_delete_env_var_not_found(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Environment variable not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_env_var("gh/CircleCI-Public/api-preview-docs", "ENV_VAR")

    @patch('requests.delete')
    def test_delete_env_var_server_error(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_env_var("gh/CircleCI-Public/api-preview-docs", "ENV_VAR")

    @patch('requests.get')
    def test_get_masked_env_var_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "ENV_VAR", "value": "masked_value"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_masked_env_var("gh/CircleCI-Public/api-preview-docs", "ENV_VAR")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"name": "ENV_VAR", "value": "masked_value"})

    @patch('requests.get')
    def test_get_masked_env_var_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Environment variable not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_masked_env_var("gh/CircleCI-Public/api-preview-docs", "ENV_VAR")

    @patch('requests.get')
    def test_get_masked_env_var_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_masked_env_var("gh/CircleCI-Public/api-preview-docs", "ENV_VAR")

    @patch('requests.post')
    def test_create_new_project_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Project created successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.create_new_project("gh", "CircleCI-Public", "api-preview-docs")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Project created successfully"})

    @patch('requests.post')
    def test_create_new_project_invalid_vcs_type(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid VCS type"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_new_project("invalid_vcs", "CircleCI-Public", "api-preview-docs")

    @patch('requests.post')
    def test_create_new_project_not_found(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Organization or repository not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_new_project("gh", "NonExistentOrg", "NonExistentRepo")

    @patch('requests.post')
    def test_create_new_project_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_new_project("gh", "CircleCI-Public", "api-preview-docs")

    @patch('requests.get')
    def test_get_project_setting_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"settings": "some_settings"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_project_setting("gh", "CircleCI-Public", "api-preview-docs")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"settings": "some_settings"})

    @patch('requests.get')
    def test_get_project_setting_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_project_setting("gh", "NonExistentOrg", "NonExistentRepo")

    @patch('requests.get')
    def test_get_project_setting_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_project_setting("gh", "CircleCI-Public", "api-preview-docs")

    @patch('requests.patch')
    def test_update_project_setting_successful(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Settings updated successfully"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.update_project_setting("gh", "CircleCI-Public", "api-preview-docs",
                                                 {"key": "value"})

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Settings updated successfully"})

    @patch('requests.patch')
    def test_update_project_setting_invalid_vcs_type(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid VCS type"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.update_project_setting("invalid_vcs", "CircleCI-Public", "api-preview-docs",
                                          {"key": "value"})

    @patch('requests.patch')
    def test_update_project_setting_not_found(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.update_project_setting("gh", "NonExistentOrg", "NonExistentRepo",
                                          {"key": "value"})

    @patch('requests.patch')
    def test_update_project_setting_server_error(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.update_project_setting("gh", "CircleCI-Public", "api-preview-docs",
                                          {"key": "value"})

    @patch('requests.get')
    def test_get_last_build_artifacts_by_project_name_successful(self, mock_get):
        mock_pipeline_response = Mock()
        mock_pipeline_response.status_code = 200
        mock_pipeline_response.json.return_value = {'items': [{'id': 'pipeline_id'}]}

        mock_workflow_response = Mock()
        mock_workflow_response.status_code = 200
        mock_workflow_response.json.return_value = {'items': [{'id': 'workflow_id'}]}

        mock_jobs_response = Mock()
        mock_jobs_response.status_code = 200
        mock_jobs_response.json.return_value = {'items': [{'job_number': 'job_number'}]}

        mock_artifacts_response = Mock()
        mock_artifacts_response.status_code = 200
        mock_artifacts_response.json.return_value = [
            {'path': 'artifact_path', 'url': 'artifact_url'}]

        mock_get.side_effect = [mock_pipeline_response, mock_workflow_response, mock_jobs_response,
                                mock_artifacts_response]

        client = CircleCI(token="dummy_token")
        response = client.get_last_build_artifacts_by_project_name(
            "gh/CircleCI-Public/api-preview-docs", "main")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {'response': [{'path': 'artifact_path', 'url': 'artifact_url'}]})

    @patch('requests.get')
    def test_get_last_build_artifacts_by_project_name_pipeline_not_found(self, mock_get):
        mock_pipeline_response = Mock()
        mock_pipeline_response.status_code = 404
        mock_pipeline_response.json.return_value = {"message": "Pipeline not found"}

        mock_get.return_value = mock_pipeline_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_last_build_artifacts_by_project_name("gh/CircleCI-Public/api-preview-docs",
                                                            "main")

    @patch('requests.get')
    def test_get_last_build_artifacts_by_project_name_workflow_not_found(self, mock_get):
        mock_pipeline_response = Mock()
        mock_pipeline_response.status_code = 200
        mock_pipeline_response.json.return_value = {'items': [{'id': 'pipeline_id'}]}

        mock_workflow_response = Mock()
        mock_workflow_response.status_code = 404
        mock_workflow_response.json.return_value = {"message": "Workflow not found"}

        mock_get.side_effect = [mock_pipeline_response, mock_workflow_response]

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_last_build_artifacts_by_project_name("gh/CircleCI-Public/api-preview-docs",
                                                            "main")

    @patch('requests.get')
    def test_get_last_build_artifacts_by_project_name_job_not_found(self, mock_get):
        mock_pipeline_response = Mock()
        mock_pipeline_response.status_code = 200
        mock_pipeline_response.json.return_value = {'items': [{'id': 'pipeline_id'}]}

        mock_workflow_response = Mock()
        mock_workflow_response.status_code = 200
        mock_workflow_response.json.return_value = {'items': [{'id': 'workflow_id'}]}

        mock_jobs_response = Mock()
        mock_jobs_response.status_code = 404
        mock_jobs_response.json.return_value = {"message": "Job not found"}

        mock_get.side_effect = [mock_pipeline_response, mock_workflow_response, mock_jobs_response]

        client = CircleCI(token="dummy_token")

        with self.assertRaises(CircleCIError):
            client.get_last_build_artifacts_by_project_name("gh/CircleCI-Public/api-preview-docs",
                                                            "main")

    @patch('requests.get')
    def test_get_last_build_artifacts_by_project_name_server_error(self, mock_get):
        mock_pipeline_response = Mock()
        mock_pipeline_response.status_code = 200
        mock_pipeline_response.json.return_value = {'items': [{'id': 'pipeline_id'}]}

        mock_workflow_response = Mock()
        mock_workflow_response.status_code = 200
        mock_workflow_response.json.return_value = {'items': [{'id': 'workflow_id'}]}

        mock_jobs_response = Mock()
        mock_jobs_response.status_code = 200
        mock_jobs_response.json.return_value = {'items': [{'job_number': 'job_number'}]}

        mock_artifacts_response = Mock()
        mock_artifacts_response.status_code = 500
        mock_artifacts_response.json.return_value = {"message": "Server Error"}

        mock_get.side_effect = [mock_pipeline_response, mock_workflow_response, mock_jobs_response,
                                mock_artifacts_response]

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_last_build_artifacts_by_project_name("gh/CircleCI-Public/api-preview-docs",
                                                            "main")
