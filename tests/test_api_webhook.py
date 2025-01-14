""" Tests for the CircleCI client. """
import unittest
from unittest.mock import patch, Mock

from circleci_api_python.client import CircleCI, CircleCIError


class TestCircleCIClient(unittest.TestCase):
    """ Tests for the CircleCI client. """

    @patch('requests.get')
    def test_get_webhooks_successful(self, mock_get: Mock) -> None:
        """
        Test get webhooks successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"webhooks": ["webhook1", "webhook2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_webhooks("scope_id", "scope_type")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"webhooks": ["webhook1", "webhook2"]})

    @patch('requests.get')
    def test_get_webhooks_not_found(self, mock_get: Mock) -> None:
        """
        Test get webhooks not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Webhooks not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_webhooks("invalid_scope_id", "scope_type")

    @patch('requests.get')
    def test_get_webhooks_server_error(self, mock_get: Mock) -> None:
        """
        Test get webhooks with server error

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
            client.get_webhooks("scope_id", "scope_type")

    @patch('requests.post')
    def test_create_outbound_webhook_successful(self, mock_post: Mock) -> None:
        """
        Test create outbound webhook successful

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
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
    def test_create_outbound_webhook_invalid_scope(self, mock_post: Mock) -> None:
        """
        Test create outbound webhook with invalid scope

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
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
    def test_create_outbound_webhook_server_error(self, mock_post: Mock) -> None:
        """
        Test create outbound webhook with server error

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
            client.create_outbound_webhook(
                name="webhook_name",
                events=["event1", "event2"],
                url="https://example.com/webhook",
                verify_tls=True,
                signing_secret="secret",
                scope={"type": "project", "id": "project_id"}
            )

    @patch('requests.get')
    def test_get_webhook_by_id_successful(self, mock_get: Mock) -> None:
        """
        Test get webhook by id successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "webhook_id", "name": "webhook_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_webhook_by_id("webhook_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "webhook_id", "name": "webhook_name"})

    @patch('requests.get')
    def test_get_webhook_by_id_not_found(self, mock_get: Mock) -> None:
        """
        Test get webhook by id not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Webhook not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_webhook_by_id("webhook_id")

    @patch('requests.get')
    def test_get_webhook_by_id_server_error(self, mock_get: Mock) -> None:
        """
        Test get webhook by id with server error

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
            client.get_webhook_by_id("webhook_id")

    @patch('requests.put')
    def test_update_webhook_by_id_successful(self, mock_put: Mock) -> None:
        """
        Test update webhook by id successful

        Args:
            mock_put (Mock): Mock object for requests.put

        Returns:
            None
        """
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
    def test_update_webhook_by_id_not_found(self, mock_put: Mock) -> None:
        """
        Test update webhook by id not found

        Args:
            mock_put (Mock): Mock object for requests.put

        Returns:
            None
        """
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
    def test_update_webhook_by_id_server_error(self, mock_put: Mock) -> None:
        """
        Test update webhook by id with server error

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
            client.update_webhook_by_id(
                webhook_id="webhook_id",
                name="new_name",
                events=["event1", "event2"],
                url="https://example.com/webhook",
                verify_tls=True,
                signing_secret="new_secret"
            )

    @patch('requests.delete')
    def test_delete_webhook_by_id_successful(self, mock_delete: Mock) -> None:
        """
        Test delete webhook by id successful

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Webhook deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_webhook_by_id("webhook_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Webhook deleted successfully"})

    @patch('requests.delete')
    def test_delete_webhook_by_id_not_found(self, mock_delete: Mock) -> None:
        """
        Test delete webhook by id not found

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Webhook not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_webhook_by_id("webhook_id")

    @patch('requests.delete')
    def test_delete_webhook_by_id_server_error(self, mock_delete: Mock) -> None:
        """
        Test delete webhook by id with server error

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
            client.delete_webhook_by_id("webhook_id")
