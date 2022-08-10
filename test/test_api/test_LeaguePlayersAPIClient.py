import unittest
from unittest import mock

from pymfl.api import LeaguePlayersAPIClient
from pymfl.api.config import APIConfig
from test.helper.helper_classes import MockResponse


class TestLeaguePlayersAPIClient(unittest.TestCase):
    __TEST_YEAR = 2020
    __TEST_LEAGUE_ID = "12345"
    __TEST_USERNAME = "username"
    __TEST_PASSWORD = "password"
    __TEST_USER_AGENT_NAME = "user_agent_name"

    @classmethod
    @mock.patch("requests.post")
    def setUpClass(cls, mock_requests_post):
        mock_xml = """<status MFL_USER_ID="test_user_id=">OK</status>"""
        mock_response = MockResponse(dict(), 200, content=mock_xml)
        mock_requests_post.return_value = mock_response
        APIConfig.add_config_for_year_and_league_id(year=cls.__TEST_YEAR,
                                                    league_id=cls.__TEST_LEAGUE_ID,
                                                    username=cls.__TEST_USERNAME,
                                                    password=cls.__TEST_PASSWORD,
                                                    user_agent_name=cls.__TEST_USER_AGENT_NAME)

    @mock.patch("requests.get")
    def test_get_player_roster_status_happy_path(self, mock_requests_get):
        mock_dict = {
            "k": "v"
        }

        mock_response = MockResponse(mock_dict, 200)
        mock_requests_get.return_value = mock_response
        response = LeaguePlayersAPIClient.get_player_roster_status(year=self.__TEST_YEAR,
                                                                   league_id=self.__TEST_LEAGUE_ID,
                                                                   player_id_or_ids="1")

        self.assertIsInstance(response, dict)
        self.assertEqual(1, len(response.keys()))
        self.assertEqual("v", response["k"])
