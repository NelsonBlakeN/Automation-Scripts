import mock
import unittest
from Utilities import get_exec_permission, Logger

# Constants
API_BASE_URL = 'https://sleepy-fortress-77799.herokuapp.com/scripts/'


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


# Helper functions
def mock_get_script(*args, **kwargs):
    if args[0] == API_BASE_URL + "valid_script":
        return MockResponse({"value": 1}, 200)
    elif args[0] == API_BASE_URL + "deny_script":
        return MockResponse({"value": 0}, 200)
    elif args[0] == API_BASE_URL + "new_script":
        return MockResponse({"value": 0}, 404)


def mock_post_script(*args, **kwargs):
    if args[0] == API_BASE_URL + "new_script/1":
        return MockResponse({"value": 1}, 200)


def mock_path_expanduser(*args, **kwargs):
    if args[0] == "~/":
        return '/home/test/'


def mock_path_exists(*args, **kwargs):
    if 'fake' not in args[0]:
        return True
    return False


# Skip creating a directory
def mock_mkdir(*args, **kwargs):
    pass


# Skip adding a log object to the logger
def mock_add_log(*args, **kwargs):
    pass


# Skip verifying the file location
def mock_verify_log_location(*args, **kwargs):
    pass


# Return mock log object
def mock_create_logger(*args, **kwargs):
    mock_handler = mock.Mock()
    mock_handler.baseFilename = args[0]
    mock_log = mock.Mock()
    mock_log.handlers = [mock_handler]
    return mock_log


def get_empty_logger():
    Logger.add_log = mock_add_log
    return Logger('default')


def mock_handler_constructor(*args, **kwargs):
    def mock_set_level(self, filename):
        self.level = filename

    def mock_add_handler(self, handler):
        pass  # Don't need to do anything with handlers yet

    handler = mock.Mock()
    handler.baseFilename = args[0]
    handler.setLevel = mock_set_level
    handler.addHandler = mock_add_handler
    return handler


# Classes


class TestGetExecutionPermission(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('requests.get', side_effect=mock_get_script)
    def test_get_exec_permission(self, mock_get):
        # Act
        val = get_exec_permission("valid_script")

        # Assert
        self.assertIn(mock.call(API_BASE_URL + "valid_script"), mock_get.call_args_list)
        self.assertEqual(val, 1)

    @mock.patch('requests.get', side_effect=mock_get_script)
    def test_get_exec_permission_deny(self, mock_get):
        try:
            # Act
            val = get_exec_permission("deny_script")

            # Assert
            self.assertIn(mock.call(API_BASE_URL + "deny_script"), mock_get.call_args_list)
            self.assertEqual(val, 0)
        except AssertionError as e:
            raise
        except Exception as e:
            self.fail("Method threw exception.")
            print(e)

    @mock.patch('requests.post', side_effect=mock_post_script)
    @mock.patch('requests.get', side_effect=mock_get_script)
    def test_get_exec_permission_dne(self, mock_get, mock_post):
        # Act
        val = get_exec_permission("new_script")

        # Assert
        self.assertIn(mock.call(API_BASE_URL + "new_script"), mock_get.call_args_list)
        self.assertIn(mock.call(API_BASE_URL + "new_script/1"), mock_post.call_args_list)

        self.assertEqual(val, 1)


class TestLogger(unittest.TestCase):
    # TODO: Potentially split this class into tests for private methods, public methods, and logging methods
    # Each of these categories have similar setups and teardowns within them so it may be useful to break them up
    # and write their respective setup and teardown classes

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('os.path.expanduser', side_effect=mock_path_expanduser)
    @mock.patch('os.path.exists', side_effect=mock_path_exists)
    def test_logger_verify_path_exists(self, mock_exists, mock_expanduser):
        # Arrange
        test_logger = get_empty_logger()

        # Act
        test_logger._Logger__verify_log_location('~/real/path/to/log')

        # Assert
        # Verify the function got through each directory level
        self.assertIn(mock.call('/home/test/real/path/to/'), mock_exists.call_args_list)

    # TODO: Mock the mkdir function so that it doesn't do anything,
    # but then check it's call args to make sure it was called with the right path
    @mock.patch('os.mkdir', side_effect=mock_mkdir)
    @mock.patch('os.path.expanduser', side_effect=mock_path_expanduser)
    @mock.patch('os.path.exists', side_effect=mock_path_exists)
    def test_logger_verify_path_dne(self, mock_exists, mock_expanduser, mock_mkdir):
        # Arrange
        test_logger = get_empty_logger()

        # Act
        test_logger._Logger__verify_log_location("~/fake/path/to/log")

        # Assert
        # Verfiy the function got through each directory level
        self.assertIn(mock.call('/home/test/fake/path/to/'), mock_exists.call_args_list)
        self.assertIn(mock.call('/home/test/fake/'), mock_mkdir.call_args_list)

    def test_add_log_no_name(self):
        # Arrange
        test_logger = Logger()

        # Act/Assert
        try:
            test_logger.add_log()
            self.fail("Expected exception to be thrown.")
        except AssertionError:
            raise
        except TypeError as e:
            self.assertIn('name', str(e))

    def test_add_log(self):
        # Arrange
        test_logger = Logger()
        # Mock location verification function
        test_logger._Logger__verify_log_location = mock_verify_log_location
        # Mock logger creation
        test_logger._Logger__create_log = mock_create_logger

        # Act
        test_logger.add_log('test_log')

        # Assert
        # Assert that a log was created
        self.assertEqual(len(test_logger.logs), 1)
        # Assert that a log was created with the correct name
        self.assertEqual(test_logger.logs[0].handlers[0].baseFilename, 'test_log')

    @mock.patch('logging.Handler', side_effect=mock_handler_constructor)
    def test_create_logger(self, mock_handler):
        # Arrange
        test_logger = Logger()

        # Act
        logger = test_logger._Logger__create_log('test_log', 'test_log.txt')

        # Assert
        # TODO: Look up the variable for a logger level
        # since I can't access the internet on an airplane, and assert it is correct
        self.assertIn(mock.call('test_log.txt'), mock_handler.call_args_list)
        self.assertEqual(logger.level, 20)

    def test_logger_log(self):
        # Arrange
        test_logger = Logger()
        test_log_a = mock.Mock()
        test_log_b = mock.Mock()
        test_logger.logs = [test_log_a, test_log_b]

        # Act
        test_logger.log('message')

        # Assert
        test_log_a.info.assert_called_with('message')
        test_log_b.info.assert_called_with('message')

    def test_logger_error(self):
        # Arrange
        test_logger = Logger()
        test_log_a = mock.Mock()
        test_log_b = mock.Mock()
        test_logger.logs = [test_log_a, test_log_b]

        # Act
        test_logger.error("error")

        # Assert
        test_log_a.error.assert_called_with("error")
        test_log_b.error.assert_called_with("error")

    def test_logger_warning(self):
        # Arrange
        test_logger = Logger()
        test_log_a = mock.Mock()
        test_log_b = mock.Mock()
        test_logger.logs = [test_log_a, test_log_b]

        # Act
        test_logger.warning("warning")

        # Assert
        test_log_a.warning.assert_called_with("warning")
        test_log_b.warning.assert_called_with("warning")

if __name__ == "__main__":
    unittest.main()