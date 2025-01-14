""" Tests for the CircleCI client context endpoints """
import unittest
from unittest.mock import patch, Mock

from circleci_api_python.client import CircleCI, CircleCIError


class TestCircleCIClient(unittest.TestCase):
    """ Tests for the CircleCI client context endpoints """

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
