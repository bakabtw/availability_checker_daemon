import unittest
from availability_checker.checker import AvailabilityChecker

host = {
    'name': 'Test server',
    'server': '127.0.0.1',
    'port': 8000,
    'method': 'http',
    'path': '/'
}


class MyTestCase(unittest.TestCase):
    def test_AvailibilityChecker_init(self):
        checker = AvailabilityChecker(host)

        expected = host
        actual = checker.host

        self.assertEqual(expected, actual)

    def test_AvailibilityChecker_init_empty(self):
        with self.assertRaises(Exception) as e:
            checker = AvailabilityChecker([])

        expected = "No host provided"
        actual = e.exception.args[0]

        self.assertEqual(expected, actual)

    def test_AvailibilityChecker_check_incorrect_method(self):
        incorrect_host = host
        incorrect_host['method'] = "unknown_method"

        print(incorrect_host)

        with self.assertRaises(Exception) as e:
            checker = AvailabilityChecker(incorrect_host).check()

        expected = "Unknown check method"
        actual = e.exception.args[0]

        self.assertEqual(expected, actual)

    def test_check_HTTP_method(self):
        checking_server = {
            'server': 'google.com',
            'port': 80,
            'method': 'http',
            'path': '/'
        }

        checker = AvailabilityChecker(checking_server).check()

        expected = {'status': 'online', 'response_code': 200}
        actual = {'status': checker['status'], 'response_code': checker['response_code']}

        self.assertEqual(expected, actual)

    def test_check_HTTPS_method(self):
        checking_server = {
            'server': 'google.com',
            'port': 443,
            'method': 'https',
            'path': '/'
        }

        checker = AvailabilityChecker(checking_server).check()

        expected = {'status': 'online', 'response_code': 200}
        actual = {'status': checker['status'], 'response_code': checker['response_code']}

        self.assertEqual(expected, actual)

    def test_check_invalid_server(self):
        checking_server = {
            'server': 'example.example',
            'port': 80,
            'method': 'http',
            'path': '/'
        }

        checker = AvailabilityChecker(checking_server).check()

        expected = {'status': 'offline'}
        actual = {'status': checker['status']}

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
