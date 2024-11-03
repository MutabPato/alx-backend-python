#!/usr/bin/env python3
"""Unittests and Integration Tests
"""


import unittest
from utils import access_nested_map
from parameterized import parameterized
from typing import Dict, Union, Tuple


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


if __name__ == "__main__":
    unittest.main()
