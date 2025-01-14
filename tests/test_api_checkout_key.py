""" Tests for the CircleCI client. """
import unittest
from unittest.mock import patch, Mock

from circleci_api_python.client import CircleCI, CircleCIError


class TestCircleCIClient(unittest.TestCase):
    """ Tests for the CircleCI client. """

    @patch('requests.post')
    def test_create_checkout_key_successful(self, mock_post: Mock) -> None:
        """
        Test create checkout key successful

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Checkout key created successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.create_checkout_key("gh/CircleCI-Public/api-preview-docs", "deploy-key")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Checkout key created successfully"})

    @patch('requests.post')
    def test_create_checkout_key_invalid_project(self, mock_post: Mock) -> None:
        """
        Test create checkout key with invalid project

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_checkout_key("gh/CircleCI-Public/nonexistent-project", "deploy-key")

    @patch('requests.post')
    def test_create_checkout_key_server_error(self, mock_post: Mock) -> None:
        """
        Test create checkout key with server error

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
            client.create_checkout_key("gh/CircleCI-Public/api-preview-docs", "deploy-key")

    @patch('requests.get')
    def test_get_all_checkout_keys_successful(self, mock_get: Mock) -> None:
        """
        Test get all checkout keys successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
    def test_get_all_checkout_keys_with_digest(self, mock_get: Mock) -> None:
        """
        Test get all checkout keys with digest

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
    def test_get_all_checkout_keys_not_found(self, mock_get: Mock) -> None:
        """
        Test get all checkout keys not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_all_checkout_keys("gh/CircleCI-Public/nonexistent-project", "")

    @patch('requests.get')
    def test_get_all_checkout_keys_server_error(self, mock_get: Mock) -> None:
        """
        Test get all checkout keys with server error

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
            client.get_all_checkout_keys("gh/CircleCI-Public/api-preview-docs", "")

    @patch('requests.delete')
    def test_delete_checkout_key_successful(self, mock_delete: Mock) -> None:
        """
        Test delete checkout key successful

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Checkout key deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_checkout_key("gh/CircleCI-Public/api-preview-docs",
                                              "fingerprint")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Checkout key deleted successfully"})

    @patch('requests.delete')
    def test_delete_checkout_key_not_found(self, mock_delete: Mock) -> None:
        """
        Test delete checkout key not found

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Checkout key not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_checkout_key("gh/CircleCI-Public/api-preview-docs",
                                       "nonexistent-fingerprint")

    @patch('requests.delete')
    def test_delete_checkout_key_server_error(self, mock_delete: Mock) -> None:
        """
        Test delete checkout key with server error

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
            client.delete_checkout_key("gh/CircleCI-Public/api-preview-docs",
                                       "fingerprint")

    @patch('requests.get')
    def test_get_checkout_key_successful(self, mock_get: Mock) -> None:
        """
        Test get checkout key successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"fingerprint": "fingerprint1", "type": "deploy-key"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_checkout_key("gh/CircleCI-Public/api-preview-docs",
                                           "fingerprint1")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"fingerprint": "fingerprint1", "type": "deploy-key"})

    @patch('requests.get')
    def test_get_checkout_key_not_found(self, mock_get: Mock) -> None:
        """
        Test get checkout key not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Checkout key not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_checkout_key("gh/CircleCI-Public/api-preview-docs",
                                    "nonexistent-fingerprint")

    @patch('requests.get')
    def test_get_checkout_key_server_error(self, mock_get: Mock) -> None:
        """
        Test get checkout key with server error

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
            client.get_checkout_key("gh/CircleCI-Public/api-preview-docs",
                                    "fingerprint1")

    @patch('requests.post')
    def test_create_env_var_successful(self, mock_post: Mock) -> None:
        """
        Test create environment variable successful

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Environment variable created successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.create_env_var("gh/CircleCI-Public/api-preview-docs",
                                         "ENV_VAR", "value")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {"message": "Environment variable created successfully"})

    @patch('requests.post')
    def test_create_env_var_invalid_project(self, mock_post: Mock) -> None:
        """
        Test create environment variable with invalid project

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_env_var("gh/CircleCI-Public/invalid-project",
                                  "ENV_VAR", "value")

    @patch('requests.post')
    def test_create_env_var_server_error(self, mock_post: Mock) -> None:
        """
        Test create environment variable with server error

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
            client.create_env_var("gh/CircleCI-Public/api-preview-docs",
                                  "ENV_VAR", "value")

    @patch('requests.get')
    def test_get_all_env_vars_successful(self, mock_get: Mock) -> None:
        """
        Test get all environment variables successful

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
        response = client.get_all_env_vars("gh/CircleCI-Public/api-preview-docs")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {'response': [{'name': 'ENV_VAR', 'value': 'value'}]})

    @patch('requests.get')
    def test_get_all_env_vars_not_found(self, mock_get: Mock) -> None:
        """
        Test get all environment variables not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_all_env_vars("gh/CircleCI-Public/api-preview-docs")

    @patch('requests.get')
    def test_get_all_env_vars_server_error(self, mock_get: Mock) -> None:
        """
        Test get all environment variables with server error

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
            client.get_all_env_vars("gh/CircleCI-Public/api-preview-docs")

    @patch('requests.delete')
    def test_delete_env_var_successful(self, mock_delete: Mock) -> None:
        """
        Test delete environment variable successful

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Environment variable deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_env_var("gh/CircleCI-Public/api-preview-docs",
                                         "ENV_VAR")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data,
                         {"message": "Environment variable deleted successfully"})

    @patch('requests.delete')
    def test_delete_env_var_not_found(self, mock_delete: Mock) -> None:
        """
        Test delete environment variable not found

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Environment variable not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_env_var("gh/CircleCI-Public/api-preview-docs",
                                  "ENV_VAR")

    @patch('requests.delete')
    def test_delete_env_var_server_error(self, mock_delete: Mock) -> None:
        """
        Test delete environment variable with server error

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
            client.delete_env_var("gh/CircleCI-Public/api-preview-docs",
                                  "ENV_VAR")

    @patch('requests.get')
    def test_get_masked_env_var_successful(self, mock_get: Mock) -> None:
        """
        Test get masked environment variable successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "ENV_VAR", "value": "masked_value"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_masked_env_var("gh/CircleCI-Public/api-preview-docs",
                                             "ENV_VAR")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"name": "ENV_VAR", "value": "masked_value"})

    @patch('requests.get')
    def test_get_masked_env_var_not_found(self, mock_get: Mock) -> None:
        """
        Test get masked environment variable not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Environment variable not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_masked_env_var("gh/CircleCI-Public/api-preview-docs",
                                      "ENV_VAR")

    @patch('requests.get')
    def test_get_masked_env_var_server_error(self, mock_get: Mock) -> None:
        """
        Test get masked environment variable with server error

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
            client.get_masked_env_var("gh/CircleCI-Public/api-preview-docs",
                                      "ENV_VAR")
