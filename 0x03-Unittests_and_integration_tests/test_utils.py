#!/usr/bin/env python3
"""Unittests and Integration Tests
"""


import unittest
from utils import access_nested_map, get_json
from parameterized import parameterized
from typing import Dict, Union, Tuple
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """Test class
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(
            self,
            nested_map: Dict,
            path: Tuple[str], expected: Union[Dict, int]) -> None:
        """Test method
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
        ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict,
            path: Tuple[str]) -> None:
        """Test method
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test class
    """
    @parameterized.expand([
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict[str, bool]
            ) -> None:
        """Test method"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            self.assertEqual(get_json(test_url), test_payload)
            mock_get.assert_called_once_with(test_url)


if __name__ == "__main__":
    unittest.main()
