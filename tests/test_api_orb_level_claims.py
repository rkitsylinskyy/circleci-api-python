""" Tests for the CircleCI client. """
import unittest
from unittest.mock import patch, Mock

from circleci.client import CircleCI, CircleCIError


class TestCircleCIClient(unittest.TestCase):
    """ Tests for the CircleCI client. """

    @patch('requests.delete')
    def test_delete_org_level_claims_successful(self, mock_delete: Mock) -> None:
        """
        Test delete org level claims successful

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Claims deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_org_level_claims("org_id", "claim1,claim2")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Claims deleted successfully"})

    @patch('requests.delete')
    def test_delete_org_level_claims_not_found(self, mock_delete: Mock) -> None:
        """
        Test delete org level claims not found

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Organization not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_org_level_claims("org_id", "claim1,claim2")

    @patch('requests.delete')
    def test_delete_org_level_claims_server_error(self, mock_delete: Mock) -> None:
        """
        Test delete org level claims with server error

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
            client.delete_org_level_claims("org_id", "claim1,claim2")

    @patch('requests.get')
    def test_get_org_level_claims_successful(self, mock_get: Mock) -> None:
        """
        Test get org level claims successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"claims": ["claim1", "claim2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_org_level_claims("org_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"claims": ["claim1", "claim2"]})

    @patch('requests.get')
    def test_get_org_level_claims_not_found(self, mock_get: Mock) -> None:
        """
        Test get org level claims not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Organization not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_org_level_claims("org_id")

    @patch('requests.get')
    def test_get_org_level_claims_server_error(self, mock_get: Mock) -> None:
        """
        Test get org level claims with server error

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
            client.get_org_level_claims("org_id")

    @patch('requests.patch')
    def test_create_or_update_org_level_claims_successful(self, mock_patch: Mock) -> None:
        """
        Test create or update org level claims successful

        Args:
            mock_patch (Mock): Mock object for requests.patch

        Returns:
            None
        """
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
    def test_create_or_update_org_level_claims_invalid_org(self, mock_patch: Mock) -> None:
        """
        Test create or update org level claims with invalid

        Args:
            mock_patch (Mock): Mock object for requests.patch

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid organization"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_or_update_org_level_claims("invalid_org_id", ["audience1", "audience2"],
                                                     "3600")

    @patch('requests.patch')
    def test_create_or_update_org_level_claims_server_error(self, mock_patch: Mock) -> None:
        """
        Test create or update org level claims with server error

        Args:
            mock_patch (Mock): Mock object for requests.patch

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_or_update_org_level_claims("org_id", ["audience1", "audience2"], "3600")

    @patch('requests.delete')
    def test_delete_project_level_claims_successful(self, mock_delete: Mock) -> None:
        """
        Test delete project level claims successful

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Claims deleted successfully"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.delete_project_level_claims("org_id", "project_id", "claim1,claim2")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Claims deleted successfully"})

    @patch('requests.delete')
    def test_delete_project_level_claims_not_found(self, mock_delete: Mock) -> None:
        """
        Test delete project level claims not found

        Args:
            mock_delete (Mock): Mock object for requests.delete

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Organization or project not found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.delete_project_level_claims("org_id", "project_id", "claim1,claim2")

    @patch('requests.delete')
    def test_delete_project_level_claims_server_error(self, mock_delete: Mock) -> None:
        """
        Test delete project level claims with server error

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
            client.delete_project_level_claims("org_id", "project_id", "claim1,claim2")

    @patch('requests.get')
    def test_get_project_level_claims_successful(self, mock_get: Mock) -> None:
        """
        Test get project level claims successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"claims": ["claim1", "claim2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_project_level_claims("org_id", "project_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"claims": ["claim1", "claim2"]})

    @patch('requests.get')
    def test_get_project_level_claims_not_found(self, mock_get: Mock) -> None:
        """
        Test get project level claims not found

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
            client.get_project_level_claims("org_id", "project_id")

    @patch('requests.get')
    def test_get_project_level_claims_server_error(self, mock_get: Mock) -> None:
        """
        Test get project level claims with server error

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
            client.get_project_level_claims("org_id", "project_id")

    @patch('requests.patch')
    def test_create_or_update_project_level_claims_successful(self, mock_patch: Mock) -> None:
        """
        Test create or update project level claims successful

        Args:
            mock_patch (Mock): Mock object for requests.patch

        Returns:
            None
        """
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
    def test_create_or_update_project_level_claims_invalid_org(self, mock_patch: Mock) -> None:
        """
        Test create or update project level claims with invalid

        Args:
            mock_patch (Mock): Mock object for requests.patch

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid organization"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_or_update_project_level_claims("invalid_org_id", "project_id",
                                                         ["audience1", "audience2"], "3600")

    @patch('requests.patch')
    def test_create_or_update_project_level_claims_server_error(self, mock_patch: Mock) -> None:
        """
        Test create or update project level claims with server error

        Args:
            mock_patch (Mock): Mock object for requests.patch

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_or_update_project_level_claims("org_id", "project_id",
                                                         ["audience1", "audience2"], "3600")
