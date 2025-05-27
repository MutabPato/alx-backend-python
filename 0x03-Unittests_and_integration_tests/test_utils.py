#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json
from unittest.mock import Mock, patch

class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for the utils..access_nested_map funtion
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, output):
        """
        Test method
        """
        self.assertEqual(access_nested_map(nested_map, path), output)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a","b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test for an exception
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):
    """
    Test class for the utils.get_json function
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        """
        mock_get.return_value.json.return_value = {"payload": True}
        for _ in mock_get(test_url):
            mock_get.json.return_value = test_payload
            mock_get.assert_called_once()