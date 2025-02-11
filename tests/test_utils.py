import os
import pytest
from unittest import TestCase
from unittest.mock import patch
from kitops.modelkit.utils import load_environment_variables, clean_empty_items, validate_dict

class TestLoadEnvironmentVariables(TestCase):

    @patch.dict(os.environ, {
        "JOZU_USERNAME": "test_user",
        "JOZU_PASSWORD": "test_password",
        "JOZU_REGISTRY": "test_registry",
        "JOZU_NAMESPACE": "test_namespace"
    })
    def test_load_environment_variables_success(self):
        expected = {
            "username": "test_user",
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
            "username": "test_user",
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


@pytest.mark.parametrize(
    "input_dict, allowed_keys, should_raise, expected_message",
    [
        ({"a": 1, "b": 2}, {"a", "b"}, False, None),
        ({"a": 1, "b": 2}, {"a"}, True, "Found unallowed key(s): b"),
        ({"a": 1, "d": 2}, {"a", "b", "c"}, True, "Found unallowed key(s): d"),
        (["a", "b"], {"a", "b"}, True, "Expected a dictionary but got list"),
    ],
)
def test_validate_dict(
    input_dict, allowed_keys, should_raise, expected_message
) -> None:
    if should_raise:
        with pytest.raises(ValueError) as excinfo:
            validate_dict(input_dict, allowed_keys)
        assert expected_message in str(excinfo.value)
    else:
        try:
            validate_dict(input_dict, allowed_keys)
        except ValueError:
            pytest.fail("validate_dict raised ValueError unexpectedly!")

@pytest.mark.parametrize(
    "d, expected",
    [
        ({"a": "", "b": "c", "d": None}, {"b": "c"}),
        (["", "a", None], ["a"]),
        ({"a": {"b": "", "c": "d"}, "e": None}, {"a": {"c": "d"}}),
        (["", ["a", None], None], [["a"]]),
        (
            {"a": ["", "b", None], "c": {"d": "", "e": "f"}},
            {"a": ["b"], "c": {"e": "f"}},
        ),
        ({"a": "b", "c": "d"}, {"a": "b", "c": "d"}),
        ({}, {}),
        ([], []),
    ],
)
def test_clean_empty_items(d, expected) -> None:
    assert clean_empty_items(d) == expected
