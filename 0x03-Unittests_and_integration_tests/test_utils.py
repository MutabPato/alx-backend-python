#!/usr/bin/env python3
"""Unittests and Integration Tests"""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import Any, Dict, List


class TestAccessNestedMap(unittest.TestCase):
    """Test Class"""

    @parameterized.expand([
        ({"a": 1}, ["a", ], 1),
        ({"a": {"b": 2}}, ["a", ], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2)
    ])
    def test_access_nested_map(
            self, nested_map:
            Dict[str, Any], path: List[str], expected: Any) -> None:
        """Test function"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ["a", ]),
        ({"a": 1}, ["a", "b"])
    ])
    def test_access_nested_map_exception(
            self, nested_map: Dict[str, Any], path: List[str]) -> None:
        """Test Error"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test the get_json function"""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get: Mock) -> None:
        """Test get_json with mocked requests.get"""

        url = 'http://example.com'
        mock_response = Mock()
        mock_response.json.return_value = {"payload": True}
        mock_get.return_value = mock_response

        result = get_json(url)
        self.assertEqual(result, {"payload": True})
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Test memoize function"""

    def test_memoize(self):
        """Test memoize"""
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_instance = TestClass()

        # Patch the a_method to count how many times it is called
        with patch.object(
                test_instance, 'a_method', wraps=test_instance
                .a_method) as mock_method:
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
