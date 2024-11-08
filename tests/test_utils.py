import os
import unittest
from unittest.mock import patch
from kitops.modelkit.utils import load_environment_variables

class TestLoadEnvironmentVariables(unittest.TestCase):

    @patch.dict(os.environ, {
        "JOZU_USERNAME": "test_user",
        "JOZU_PASSWORD": "test_password",
        "JOZU_REGISTRY": "test_registry",
        "JOZU_NAMESPACE": "test_namespace"
    })
    def test_load_environment_variables_success(self):
        expected = {
            "user": "test_user",
            "password": "test_password",
            "registry": "test_registry",
            "namespace": "test_namespace"
        }
        result = load_environment_variables()
        self.assertEqual(result, expected)

    @patch.dict(os.environ, {
        "JOZU_USERNAME": "test_user",
        "JOZU_PASSWORD": "test_password"
    })
    def test_load_environment_variables_missing_optional(self):
        expected = {
            "user": "test_user",
            "password": "test_password",
            "registry": None,
            "namespace": None
        }
        result = load_environment_variables()
        self.assertEqual(result, expected)

    @patch.dict(os.environ, {
        "JOZU_USERNAME": "test_user"
    })
    def test_load_environment_variables_missing_password(self):
        with self.assertRaises(ValueError) as context:
            load_environment_variables()
        self.assertIn("Missing JOZU_USERNAME or JOZU_PASSWORD", str(context.exception))

    @patch.dict(os.environ, {
        "JOZU_PASSWORD": "test_password"
    })
    def test_load_environment_variables_missing_username(self):
        with self.assertRaises(ValueError) as context:
            load_environment_variables()
        self.assertIn("Missing JOZU_USERNAME or JOZU_PASSWORD", str(context.exception))

if __name__ == "__main__":
    unittest.main()