""" Tests for the CircleCI client. """
import unittest
from unittest.mock import patch, Mock

from circleci_api_python.client import CircleCI, CircleCIError


class TestCircleCIClient(unittest.TestCase):
    """ Tests for the CircleCI client. """

    @patch('requests.get')
    def test_get_workflow_by_id_successful(self, mock_get: Mock) -> None:
        """
        Test get workflow by id successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "workflow_id", "name": "workflow_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_workflow_by_id("workflow_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "workflow_id", "name": "workflow_name"})

    @patch('requests.get')
    def test_get_workflow_by_id_not_found(self, mock_get: Mock) -> None:
        """
        Test get workflow by id not found

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
            client.get_workflow_by_id("invalid_workflow_id")

    @patch('requests.get')
    def test_get_workflow_by_id_server_error(self, mock_get: Mock) -> None:
        """
        Test get workflow by id with server error

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
            client.get_workflow_by_id("workflow_id")

    @patch('requests.post')
    def test_approve_workflow_job_successful(self, mock_post: Mock) -> None:
        """
        Test approve workflow job successful

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Job approved successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.approve_workflow_job("workflow_id", "job_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Job approved successfully"})

    @patch('requests.post')
    def test_approve_workflow_job_not_found(self, mock_post: Mock) -> None:
        """
        Test approve workflow job not found

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Workflow or job not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.approve_workflow_job("invalid_workflow_id", "invalid_job_id")

    @patch('requests.post')
    def test_approve_workflow_job_server_error(self, mock_post: Mock) -> None:
        """
        Test approve workflow job with server error

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
            client.approve_workflow_job("workflow_id", "job_id")

    @patch('requests.post')
    def test_cancel_workflow_successful(self, mock_post: Mock) -> None:
        """
        Test cancel workflow successful

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Workflow cancelled successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.cancel_workflow("workflow_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Workflow cancelled successfully"})

    @patch('requests.post')
    def test_cancel_workflow_not_found(self, mock_post: Mock) -> None:
        """
        Test cancel workflow not found

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Workflow not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.cancel_workflow("invalid_workflow_id")

    @patch('requests.post')
    def test_cancel_workflow_server_error(self, mock_post: Mock) -> None:
        """
        Test cancel workflow with server error

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
            client.cancel_workflow("workflow_id")

    @patch('requests.get')
    def test_get_all_jobs_for_workflow_successful(self, mock_get: Mock) -> None:
        """
        Test get all jobs for workflow successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jobs": ["job1", "job2"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_workflow_jobs("workflow_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"jobs": ["job1", "job2"]})

    @patch('requests.get')
    def test_get_all_jobs_for_workflow_with_page_token(self, mock_get: Mock) -> None:
        """
        Test get all jobs for workflow with page token

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jobs": ["job1"]}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_workflow_jobs("workflow_id", page_token="token")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"jobs": ["job1"]})

    @patch('requests.get')
    def test_get_all_jobs_for_workflow_not_found(self, mock_get: Mock) -> None:
        """
        Test get all jobs for workflow not found

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
            client.get_workflow_jobs("invalid_workflow_id")

    @patch('requests.get')
    def test_get_all_jobs_for_workflow_server_error(self, mock_get: Mock) -> None:
        """
        Test get all jobs for workflow with server error

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
            client.get_workflow_jobs("workflow_id")

    @patch('requests.post')
    def test_rerun_workflow_successful(self, mock_post: Mock) -> None:
        """
        Test rerun workflow successful

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Workflow rerun successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.rerun_workflow("workflow_id")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Workflow rerun successfully"})

    @patch('requests.post')
    def test_rerun_workflow_with_ssh(self, mock_post: Mock) -> None:
        """
        Test rerun workflow with SSH

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Workflow rerun with SSH successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.rerun_workflow("workflow_id", enable_ssh=True)

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Workflow rerun with SSH successfully"})

    @patch('requests.post')
    def test_rerun_workflow_from_failed(self, mock_post: Mock) -> None:
        """
        Test rerun workflow from failed

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Workflow rerun from failed successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.rerun_workflow("workflow_id", from_failed=True)

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Workflow rerun from failed successfully"})

    @patch('requests.post')
    def test_rerun_workflow_with_jobs(self, mock_post: Mock) -> None:
        """
        Test rerun workflow with jobs

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
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
    def test_rerun_workflow_not_found(self, mock_post: Mock) -> None:
        """
        Test rerun workflow not found

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Workflow not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.rerun_workflow("invalid_workflow_id")

    @patch('requests.post')
    def test_rerun_workflow_server_error(self, mock_post: Mock) -> None:
        """
        Test rerun workflow with server error

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
            client.rerun_workflow("workflow_id")
