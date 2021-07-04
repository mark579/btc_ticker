from requests.api import get
import responses

from unittest import TestCase
from crypto import get_latest_price
from crypto import TICKER_API_URL

from requests.exceptions import ConnectionError

def mock_response(id, currency, value):
    return { id: { currency: value} }


class TestCrypto(TestCase):
    @responses.activate
    def test_get_latest_price(self):
        id = 'btc'
        vs_currency = 'usd'
        responses.add(responses.GET, f'{TICKER_API_URL}/?ids={id}&vs_currencies={vs_currency}',
                      json=mock_response(id, vs_currency, 512345.0), status=200)

        self.assertEqual(get_latest_price(id, vs_currency), '$512,345')

        id = 'doge'
        vs_currency = 'usd'
        responses.add(responses.GET, f'{TICKER_API_URL}/?ids={id}&vs_currencies={vs_currency}',
                json=mock_response(id, vs_currency, 0.223432), status=200)
        self.assertEqual(get_latest_price(id, vs_currency), '$0.223432')


    @responses.activate
    def test_get_latest_price_error(self):
        self.assertRaises(ConnectionError, get_latest_price, 'btc', 'usd')