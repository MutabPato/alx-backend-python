#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """
    Test class
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
