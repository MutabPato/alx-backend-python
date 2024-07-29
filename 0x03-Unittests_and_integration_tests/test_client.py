#!/usr/bin/env python3
"""Unittests and Integration Tests"""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from client import GithubOrgClient
from typing import Any, Dict, List


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
            ("google", {"name": "Google"}),
            ("abc", {"name": "ABC"})
    ])
    @patch('client.get_json', return_value={"name": "Mock Org"})
    def test_org(
            self, org_name: str, expected: Dict, mock_get_json: patch) -> None:
        """Test that GithubOrgClient.org returns the correct value"""
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, {"name": "Mock Org"})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    unittest.main()
