from requests.api import get
import responses

from unittest import TestCase
from jokes import get_joke
from jokes import JOKE_API_URL

from requests.exceptions import ConnectionError


def mock_json():
    return {'setup': 'HI', 'punchline': 'BYE'}


class TestJokes(TestCase):
    @responses.activate
    def test_get_joke(self):
        responses.add(responses.GET, JOKE_API_URL,
                      json=mock_json(), status=200)

        self.assertEqual(get_joke(), 'HI.....BYE')

    @responses.activate
    def test_get_joke_error(self):
        self.assertRaises(ConnectionError, get_joke)