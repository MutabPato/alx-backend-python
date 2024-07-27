#!/usr/bin/env python3
"""Unittests and Integration Tests"""


from utils import access_nested_map


Class TestAccessNestedMap(unittest.TestCase):
    """Test Class"""

    @parameterized.expand([
        (nested_map={"a": 1}, path=("a",)),
        (nested_map={"a": {"b": 2}}, path=("a",)),
        (nested_map={"a": {"b": 2}}, path=("a", "b"))
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test function"""
        self.assertEqual(test_access_nested_map(nested_map, path, expected))
