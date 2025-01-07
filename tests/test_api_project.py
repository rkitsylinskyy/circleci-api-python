""" Tests for the CircleCI client. """
import unittest
from unittest.mock import patch, Mock

from circleci.client import CircleCI, CircleCIError


class TestCircleCIClient(unittest.TestCase):
    """ Tests for the CircleCI client. """

    @patch('requests.get')
    def test_get_project_successful(self, mock_get: Mock) -> None:
        """
        Test get project successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "project_id", "name": "project_name"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_project("gh/CircleCI-Public/api-preview-docs")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"id": "project_id", "name": "project_name"})

    @patch('requests.get')
    def test_get_project_not_found(self, mock_get: Mock) -> None:
        """
        Test get project not found

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
            client.get_project("gh/CircleCI-Public/nonexistent-project")

    @patch('requests.get')
    def test_get_project_server_error(self, mock_get: Mock) -> None:
        """
        Test get project with server error

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
            client.get_project("gh/CircleCI-Public/api-preview-docs")

    @patch('requests.post')
    def test_create_new_project_successful(self, mock_post: Mock) -> None:
        """
        Test create new project successful

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Project created successfully"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.create_new_project("gh", "CircleCI-Public",
                                             "api-preview-docs")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Project created successfully"})

    @patch('requests.post')
    def test_create_new_project_invalid_vcs_type(self, mock_post: Mock) -> None:
        """
        Test create new project with invalid VCS type

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid VCS type"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_new_project("invalid_vcs", "CircleCI-Public",
                                      "api-preview-docs")

    @patch('requests.post')
    def test_create_new_project_not_found(self, mock_post: Mock) -> None:
        """
        Test create new project not found

        Args:
            mock_post (Mock): Mock object for requests.post

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Organization or repository not found"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.create_new_project("gh", "NonExistentOrg",
                                      "NonExistentRepo")

    @patch('requests.post')
    def test_create_new_project_server_error(self, mock_post: Mock) -> None:
        """
        Test create new project with server error

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
            client.create_new_project("gh", "CircleCI-Public",
                                      "api-preview-docs")

    @patch('requests.get')
    def test_get_project_setting_successful(self, mock_get: Mock) -> None:
        """
        Test get project setting successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"settings": "some_settings"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.get_project_setting("gh", "CircleCI-Public",
                                              "api-preview-docs")

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"settings": "some_settings"})

    @patch('requests.get')
    def test_get_project_setting_not_found(self, mock_get: Mock) -> None:
        """
        Test get project setting not found

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
            client.get_project_setting("gh", "NonExistentOrg",
                                       "NonExistentRepo")

    @patch('requests.get')
    def test_get_project_setting_server_error(self, mock_get: Mock) -> None:
        """
        Test get project setting with server error

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
            client.get_project_setting("gh", "CircleCI-Public",
                                       "api-preview-docs")

    @patch('requests.patch')
    def test_update_project_setting_successful(self, mock_patch: Mock) -> None:
        """
        Test update project setting successful

        Args:
            mock_patch (Mock): Mock object for requests.patch

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Settings updated successfully"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client.update_project_setting("gh", "CircleCI-Public",
                                                 "api-preview-docs",
                                                 {"key": "value"})

        self.assertEqual(response.metadata.status_code, 200)
        self.assertEqual(response.raw_data, {"message": "Settings updated successfully"})

    @patch('requests.patch')
    def test_update_project_setting_invalid_vcs_type(self, mock_patch: Mock) -> None:
        """
        Test update project setting with invalid VCS type

        Args:
            mock_patch (Mock): Mock object for requests.patch

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid VCS type"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.update_project_setting("invalid_vcs", "CircleCI-Public",
                                          "api-preview-docs",
                                          {"key": "value"})

    @patch('requests.patch')
    def test_update_project_setting_not_found(self, mock_patch: Mock) -> None:
        """
        Test update project setting not found

        Args:
            mock_patch (Mock): Mock object for requests.patch

        Returns:
            None
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Project not found"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.update_project_setting("gh", "NonExistentOrg",
                                          "NonExistentRepo",
                                          {"key": "value"})

    @patch('requests.patch')
    def test_update_project_setting_server_error(self, mock_patch: Mock) -> None:
        """
        Test update project setting with server error

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
            client.update_project_setting("gh", "CircleCI-Public",
                                          "api-preview-docs",
                                          {"key": "value"})

    @patch('requests.get')
    def test_get_last_build_artifacts_by_project_name_successful(self, mock_get: Mock) -> None:
        """
        Test get last build artifacts by project name successful

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
    def test_get_last_build_artifacts_by_project_name_pipeline_not_found(self,
                                                                         mock_get: Mock) -> None:
        """
        Test get last build artifacts by project name pipeline not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
        mock_pipeline_response = Mock()
        mock_pipeline_response.status_code = 404
        mock_pipeline_response.json.return_value = {"message": "Pipeline not found"}

        mock_get.return_value = mock_pipeline_response

        client = CircleCI(token="dummy_token")
        with self.assertRaises(CircleCIError):
            client.get_last_build_artifacts_by_project_name("gh/CircleCI-Public/api-preview-docs",
                                                            "main")

    @patch('requests.get')
    def test_get_last_build_artifacts_by_project_name_workflow_not_found(self,
                                                                         mock_get: Mock) -> None:
        """
        Test get last build artifacts by project name workflow not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
    def test_get_last_build_artifacts_by_project_name_job_not_found(self, mock_get: Mock) -> None:
        """
        Test get last build artifacts by project name job not found

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
    def test_get_last_build_artifacts_by_project_name_server_error(self, mock_get: Mock) -> None:
        """
        Test get last build artifacts by project name with server error

        Args:
            mock_get (Mock): Mock object for requests.get

        Returns:
            None
        """
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
