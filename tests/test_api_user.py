""" Tests for the CircleCI client. """
import unittest
from unittest.mock import patch, Mock

from circleci.client import CircleCI, CircleCIError


class TestCircleCIClient(unittest.TestCase):
    """ Tests for the CircleCI client. """

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
