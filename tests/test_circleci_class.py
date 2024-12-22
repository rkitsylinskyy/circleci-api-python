import unittest
from unittest.mock import patch, Mock

from circleci import CircleCIError
from circleci.client import CircleCI


class TestCircleCIClient(unittest.TestCase):

    # --------------------------------- GET REQUEST ---------------------------------
    @patch('requests.get')
    def test_get_request_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._get("/dummy_endpoint")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"key": "value"})

    @patch('requests.get')
    def test_get_request_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not Found"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._get("/dummy_endpoint")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "Not Found"})

    @patch('requests.get')
    def test_get_request_server_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_get.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._get("/dummy_endpoint")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"message": "Server Error"})

    # --------------------------------- POST REQUEST ---------------------------------
    @patch('requests.post')
    def test_post_request_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"key": "value"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._post("/dummy_endpoint", {"data": "value"})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"key": "value"})

    @patch('requests.post')
    def test_post_request_no_payload(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._post("/dummy_endpoint")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"key": "value"})

    @patch('requests.post')
    def test_post_request_server_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_post.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._post("/dummy_endpoint", {"data": "value"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"message": "Server Error"})

    # --------------------------------- DELETE REQUEST ---------------------------------

    @patch('requests.delete')
    def test_delete_request_successful(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._delete("/dummy_endpoint")

        self.assertEqual(response.status_code, 204)

    @patch('requests.delete')
    def test_delete_request_not_found(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not Found"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._delete("/dummy_endpoint")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "Not Found"})

    @patch('requests.delete')
    def test_delete_request_server_error(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_delete.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._delete("/dummy_endpoint")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"message": "Server Error"})

    # --------------------------------- PATCH REQUEST ---------------------------------

    @patch('requests.patch')
    def test_patch_request_successful(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._patch("/dummy_endpoint", {"data": "value"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"key": "value"})

    @patch('requests.patch')
    def test_patch_request_not_found(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not Found"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._patch("/dummy_endpoint", {"data": "value"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "Not Found"})

    @patch('requests.patch')
    def test_patch_request_server_error(self, mock_patch):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_patch.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._patch("/dummy_endpoint", {"data": "value"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"message": "Server Error"})

    # --------------------------------- PUT REQUEST ---------------------------------

    @patch('requests.put')
    def test_put_request_successful(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_put.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._put("/dummy_endpoint", {"data": "value"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"key": "value"})

    @patch('requests.put')
    def test_put_request_not_found(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not Found"}
        mock_put.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._put("/dummy_endpoint", {"data": "value"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "Not Found"})

    @patch('requests.put')
    def test_put_request_server_error(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server Error"}
        mock_put.return_value = mock_response

        client = CircleCI(token="dummy_token")
        response = client._put("/dummy_endpoint", {"data": "value"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"message": "Server Error"})

    # --------------------------------- DECORATOR ---------------------------------

    @patch('circleci.client.dict_to_circleci_resource')
    def test_response_validation_successful_dict(self, mock_dict_to_circleci_resource):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_dict_to_circleci_resource.return_value = {"key": "value",
                                                       "metadata": {"status_code": 200,
                                                                    "url": "http://example.com"}}

        client = CircleCI(token="dummy_token")
        client.log = Mock()

        @CircleCI.response_validation
        def dummy_method(test):
            print(test)
            return mock_response

        response = dummy_method(client)
        self.assertEqual(response, {"key": "value",
                                    "metadata": {"status_code": 200, "url": "http://example.com"}})

    @patch('circleci.client.dict_to_circleci_resource')
    def test_response_validation_successful_list(self, mock_dict_to_circleci_resource):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"key": "value"}]
        mock_dict_to_circleci_resource.return_value = {"response": [{"key": "value"}],
                                                       "metadata": {"status_code": 200,
                                                                    "url": "http://example.com"}}

        client = CircleCI(token="dummy_token")
        client.log = Mock()

        @CircleCI.response_validation
        def dummy_method(test):
            print(test)
            return mock_response

        response = dummy_method(client)
        self.assertEqual(response, {"response": [{"key": "value"}],
                                    "metadata": {"status_code": 200, "url": "http://example.com"}})

    def test_response_validation_failure(self):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Bad Request"}

        client = CircleCI(token="dummy_token")
        client.log = Mock()

        @CircleCI.response_validation
        def dummy_method(test):
            print(test)
            return mock_response

        with self.assertRaises(CircleCIError):
            dummy_method(client)


if __name__ == '__main__':
    unittest.main()
