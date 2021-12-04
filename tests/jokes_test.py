import responses

from unittest import TestCase
from jokes import build_url, get_joke
from jokes import JOKE_API_URL

from requests.exceptions import ConnectionError


def mock_json(type):
    if type == 'single':
        return {'type': 'single', 'joke': 'IMMA JOKE'}
    elif type == 'twopart':
        return {'type': 'twopart', 'setup': 'IMMA JOKE',
                'delivery': 'IMMA DELIVERY'}


class TestJokes(TestCase):
    @responses.activate
    def test_get_single_joke(self):
        responses.add(responses.GET, build_url(),
                      json=mock_json('single'), status=200)

        self.assertEqual(get_joke(), 'IMMA JOKE')

    @responses.activate
    def test_get_twopart_joke(self):
        responses.add(responses.GET, build_url(),
                      json=mock_json('twopart'), status=200)
        self.assertEqual(get_joke(), 'IMMA JOKE.....IMMA DELIVERY')

    @responses.activate
    def test_get_joke_error(self):
        self.assertRaises(ConnectionError, get_joke)
