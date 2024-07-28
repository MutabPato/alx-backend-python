#!/usr/bin/env python3
"""Unittests and Integration Tests"""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Test Class"""

    @parameterized.expand([
        ({"a": 1}, ["a", ], 1),
        ({"a": {"b": 2}}, ["a", ], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test function"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ["a", ]),
        ({"a": 1}, ["a", "b"])
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test Error"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test json class"""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """Test get_json function"""

        url = 'http://example.com'
        mock_response = Mock()
        mock_response.json.return_value = {"payload": True}
        mock_get.return_value = mock_response

        result = get_json(url)
        self.assertEqual(result, {"payload": True})
        mock_get.assert_called_once_with(url)


if __name__ == "__main__":
    unittest.main()
