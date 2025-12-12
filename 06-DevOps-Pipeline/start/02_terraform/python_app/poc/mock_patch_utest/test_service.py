# test_service.py
import unittest
from unittest import mock
import requests # Import requests here for mock.patch.object example later

# Import the functions from your service.py
from service import get_data_from_api, process_data

class TestService(unittest.TestCase):

    # --- 1. Using mock.patch as a Decorator ---
    # Patching 'requests.get' where it's used (in service.py)
    @mock.patch('service.requests.get')
    def test_get_data_from_api_success(self, mock_get):
        """
        Test successful API call using a decorator patch.
        """
        # Configure the mock object's behavior
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success", "data": "test_data"}
        mock_response.raise_for_status.return_value = None # No HTTPError
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_data_from_api("http://test.com/api")

        # Assertions
        mock_get.assert_called_once_with("http://test.com/api", timeout=5)
        self.assertEqual(result, {"status": "success", "data": "test_data"})

    @mock.patch('service.requests.get')
    def test_get_data_from_api_network_error(self, mock_get):
        """
        Test API call failure due to network error.
        """
        # Configure the mock to raise an exception
        mock_get.side_effect = requests.exceptions.ConnectionError("Mocked Connection Error")

        result = get_data_from_api("http://test.com/api")

        mock_get.assert_called_once_with("http://test.com/api", timeout=5)
        self.assertIsNone(result)

    # --- 2. Using mock.patch as a Context Manager ---
    def test_process_data_with_context_manager(self):
        """
        Test process_data using a context manager patch for get_data_from_api.
        """
        with mock.patch('service.get_data_from_api') as mock_get_data:
            mock_get_data.return_value = {"status": "ok"}

            result = process_data("http://test.com/data")

            mock_get_data.assert_called_once_with("http://test.com/data")
            self.assertEqual(result, "Processed: ok")

    # --- 3. Using mock.patch.object for patching attributes/methods of an object ---
    # This is often used when you have an instance of a class and want to mock its methods
    # or when patching an imported module's attribute.
    # Note: For 'requests.get', patching 'service.requests.get' is usually cleaner.
    # This example demonstrates patching `requests.get` directly, which would only work
    # if `requests` was imported *inside* the function being tested, or if you're testing
    # code that directly uses the global `requests` import.
    # A more common use for patch.object is to mock a method on an *instance* of a class.
    def test_get_data_from_api_timeout_with_patch_object(self):
        """
        Demonstrates patching an object's attribute/method using mock.patch.object.
        """
        # Patch the 'get' method of the 'requests' module directly.
        # This works if the code being tested uses 'requests.get' directly,
        # or if 'requests' is imported at the top level of the test file.
        # For patching dependencies *within* another module, 'module.dependency.method' is preferred.
        with mock.patch.object(requests, 'get') as mock_requests_get:
            mock_requests_get.side_effect = requests.exceptions.Timeout("Mocked Timeout")

            result = get_data_from_api("http://test.com/timeout")

            mock_requests_get.assert_called_once_with("http://test.com/timeout", timeout=5)
            self.assertIsNone(result)

    # --- 4. Manual Patching (using setUp/tearDown) ---
    # Useful when you need to patch the same thing across multiple tests in a class
    # but don't want to use a decorator on every method.
    def setUp(self):
        # Create a patcher for 'service.requests.get'
        self.patcher_get = mock.patch('service.requests.get')
        # Start the patch, get the mock object
        self.mock_get = self.patcher_get.start()

        # Configure default behavior for the mock
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "default_success"}
        mock_response.raise_for_status.return_value = None
        self.mock_get.return_value = mock_response

    def tearDown(self):
        # Stop the patch, restoring the original object
        self.patcher_get.stop()

    def test_get_data_from_api_manual_patch(self):
        """
        Test using manual patching from setUp/tearDown.
        """
        result = get_data_from_api("http://test.com/manual")
        self.mock_get.assert_called_once_with("http://test.com/manual", timeout=5)
        self.assertEqual(result, {"status": "default_success"})

    def test_get_data_from_api_manual_patch_override(self):
        """
        Test using manual patching but overriding behavior for a specific test.
        """
        # Override the return value for this specific test
        override_response = mock.Mock()
        override_response.status_code = 404
        override_response.json.return_value = {"error": "not found"}
        override_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        self.mock_get.return_value = override_response

        result = get_data_from_api("http://test.com/override")
        self.mock_get.assert_called_once_with("http://test.com/override", timeout=5)
        self.assertIsNone(result) # Because raise_for_status() will be called, leading to None

if __name__ == '__main__':
    unittest.main()
