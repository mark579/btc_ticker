from requests.api import get
import responses

from unittest import TestCase
from crypto import get_latest_price
from crypto import TICKER_API_URL

from requests.exceptions import ConnectionError

def mock_json():
    return {'btc': { 'usd': '512345'} }


class TestCrypt(TestCase):
    @responses.activate
    def test_get_latest_price(self):
        id = 'btc'
        vs_currency = 'usd'
        responses.add(responses.GET, f'{TICKER_API_URL}/?ids={id}&vs_currencies={vs_currency}',
                      json=mock_json(), status=200)

        self.assertEqual(get_latest_price(id, vs_currency), '$512,345')

    @responses.activate
    def test_get_latest_price_error(self):
        self.assertRaises(ConnectionError, get_latest_price, 'btc', 'usd')