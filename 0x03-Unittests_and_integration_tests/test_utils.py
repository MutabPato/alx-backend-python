#!/usr/bin/env python3
"""Unittests and Integration Tests
"""


import unittest
from utils import access_nested_map
from parameterized import parameterized


@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), 2),
    ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
class TestAccessNestedMap(unittest.TestCase):
    """Test class
    """
    def test_access_nested_map():
        """Test method
        """
        assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == "__main__":
    unittest.main()
