import app
import unittest

from mock import patch


class DockerPullerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        config_dict = {
                "host": "localhost",
                "port": 8000,
                "token": "abc123",
                "hooks": {
                    "hello": "scripts/hello.sh"
                }
            }
        app.config = config_dict

    def test_get_api_version(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        assert 'Version' in response.data
        
    @patch('subprocess.call')
    def test_valid_token_and_hook(self, subprocess_call):
        response = self.app.post("/abc123/hello", environ_base={"REMOTE_ADDR": "127.0.0.1"})
        self.assertEqual(response.status_code, 200)
        subprocess_call.assert_called_once_with(["scripts/hello.sh", "127.0.0.1"])

    def test_invalid_token(self):
        response = self.app.post("/abc123456/hello")
        self.assertEqual(response.status_code, 403)
        assert "Invalid token" in response.data

    def test_invalid_hook(self):
        response = self.app.post("/abc123/wronghook")
        self.assertEqual(response.status_code, 404)
        assert "Hook not found" in response.data

    def test_hook_not_specified(self):
        response = self.app.post("/abc123")
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
