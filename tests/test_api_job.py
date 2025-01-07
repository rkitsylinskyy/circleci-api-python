""" Tests for the CircleCI client. """
import unittest
from unittest.mock import patch, Mock

from circleci.client import CircleCI, CircleCIError


class TestCircleCIClient(unittest.TestCase):
    """ Tests for the CircleCI client. """

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
    def test_get_job_by_number_server_error(self, mock_get: Mock) -> None:
        """
        Test get job by number with server error

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
            client.get_job_by_number("gh/CircleCI-Public/api-preview-docs", 1)

    @patch('requests.post')
    def test_cancel_job_by_number_successful(self, mock_post: Mock) -> None:
        """
        Test cancel job by number successful

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
        response = client.cancel_job_by_number("gh/CircleCI-Public/api-preview-docs", 1)

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Job cancelled successfully"})

    @patch('requests.post')
    def test_cancel_job_by_number_not_found(self, mock_post: Mock) -> None:
        """
        Test cancel job by number not found

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
            client.cancel_job_by_number("gh/CircleCI-Public/api-preview-docs", 999)

    @patch('requests.post')
    def test_cancel_job_by_number_server_error(self, mock_post: Mock) -> None:
        """
        Test cancel job by number with server error

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
            client.cancel_job_by_number("gh/CircleCI-Public/api-preview-docs", 1)

    @patch('requests.get')
    def test_get_job_artifacts_successful(self, mock_get: Mock) -> None:
        """
        Test get job artifacts successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
    def test_get_job_artifacts_not_found(self, mock_get: Mock) -> None:
        """
        Test get job artifacts not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Artifacts not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_job_artifacts("gh/CircleCI-Public/api-preview-docs", "999")

    @patch('requests.get')
    def test_get_job_artifacts_server_error(self, mock_get: Mock) -> None:
        """
        Test get job artifacts with server error

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
            client.get_job_artifacts("gh/CircleCI-Public/api-preview-docs", "1")

    @patch('requests.get')
    def test_get_job_metadata_successful(self, mock_get: Mock) -> None:
        """
        Test get job metadata successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"tests": ["test1", "test2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_job_metadata("gh/CircleCI-Public/api-preview-docs", "1")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"tests": ["test1", "test2"]})

    @patch('requests.get')
    def test_get_job_metadata_not_found(self, mock_get: Mock) -> None:
        """
        Test get job metadata not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Job metadata not found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_job_metadata("gh/CircleCI-Public/api-preview-docs", "999")

    @patch('requests.get')
    def test_get_job_metadata_server_error(self, mock_get: Mock) -> None:
        """
        Test get job metadata with server error

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
            client.get_job_metadata("gh/CircleCI-Public/api-preview-docs", "1")
