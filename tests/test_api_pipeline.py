""" Tests for the CircleCI client. """
import unittest
from unittest.mock import patch, Mock

from circleci_api_python.client import CircleCI, CircleCIError


class TestCircleCIClient(unittest.TestCase):
    """ Tests for the CircleCI client. """

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
