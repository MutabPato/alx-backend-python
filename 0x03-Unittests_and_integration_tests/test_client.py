#!/usr/bin/env python3

"""
Test suite for client.py
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test class for client.GithubOrgClient
    """
    @parameterized.expand([
        ('google', {
            'login': 'google', 'id': 1342004,
            'node_id': 'MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ=',
            'url': 'https://api.github.com/orgs/google',
            'repos_url': 'https://api.github.com/orgs/google/repos',
            'events_url': 'https://api.github.com/orgs/google/events',
            'hooks_url': 'https://api.github.com/orgs/google/hooks',
            'issues_url': 'https://api.github.com/orgs/google/issues',
            'members_url': 'https://api.github.com/' +
            'orgs/google/members{/member}',
            'public_members_url': 'https://api.github.com/' +
            'orgs/google/public_members{/member}',
            'avatar_url': 'https://avatars.githubusercontent.com/' +
            'u/1342004?v=4',
            'description': 'Google ❤️ Open Source', 'name': 'Google',
            'company': None, 'blog': 'https://opensource.google/',
            'location': 'United States of America',
            'email': 'opensource@google.com', 'twitter_username': 'GoogleOSS',
            'is_verified': True, 'has_organization_projects': True,
            'has_repository_projects': True, 'public_repos': 2770,
            'public_gists': 0, 'followers': 54958, 'following': 0,
            'html_url': 'https://github.com/google',
            'created_at': '2012-01-18T01:30:18Z',
            'updated_at': '2024-08-09T17:36:18Z',
            'archived_at': None, 'type': 'Organization'}),
        ('abc', {
            'message': 'Not Found',
            'documentation_url': 'https://docs.github.com/' +
            'rest/orgs/orgs#get-an-organization',
            'status': '404'
            }),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, response_msg, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        mock_get_json.return_value = response_msg
        new_client = GithubOrgClient(org_name)
        output = new_client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
            )
        self.assertDictEqual(output, response_msg)

    def test_public_repos_url(self):
        """
        Test method for GithubOrgClient._public_repos_url
        """
        with patch(
            'client.GithubOrgClient.org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                'login': 'google', 'id': 1342004,
                'node_id': 'MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ=',
                'url': 'https://api.github.com/orgs/google',
                'repos_url': 'https://api.github.com/orgs/google/repos',
                'events_url': 'https://api.github.com/orgs/google/events',
                'hooks_url': 'https://api.github.com/orgs/google/hooks',
                'issues_url': 'https://api.github.com/orgs/google/issues',
                'members_url': 'https://api.github.com/' +
                'orgs/google/members{/member}',
                'public_members_url': 'https://api.github.com/' +
                'orgs/google/public_members{/member}',
                'avatar_url': 'https://avatars.githubusercontent.com/' +
                'u/1342004?v=4',
                'description': 'Google ❤️ Open Source', 'name': 'Google',
                'company': None, 'blog': 'https://opensource.google/',
                'location': 'United States of America',
                'email': 'opensource@google.com',
                'twitter_username': 'GoogleOSS',
                'is_verified': True, 'has_organization_projects': True,
                'has_repository_projects': True, 'public_repos': 2770,
                'public_gists': 0, 'followers': 54958, 'following': 0,
                'html_url': 'https://github.com/google',
                'created_at': '2012-01-18T01:30:18Z',
                'updated_at': '2024-08-09T17:36:18Z',
                'archived_at': None, 'type': 'Organization'
                }

            new_client = GithubOrgClient('google')
            url = new_client._public_repos_url
            self.assertEqual(url, 'https://api.github.com/orgs/google/repos')
