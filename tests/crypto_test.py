import responses

import os
from unittest import TestCase
from crypto import Crypto
from crypto import TICKER_API_URL

from requests.exceptions import ConnectionError


def mock_response(id, currency, value):
    return {id: {currency: value}}


class TestCrypto(TestCase):
    @responses.activate
    def test_get_latest_price(self):
        id = 'btc'
        currency = 'usd'
        responses.add(responses.GET, f'{TICKER_API_URL}/coins/list',
                      json=[{'id': 'btc', 'symbol': 'BITCOIN'},
                            {'id': 'doge', 'symbol': 'DOGE'}], status=200)
        c = Crypto()

        responses.add(responses.GET,
                      f'{TICKER_API_URL}/simple/price/' +
                      f'?ids={id}&vs_currencies={currency}',
                      json=mock_response(id, currency, 512345.0), status=200)

        self.assertEqual(c.get_latest_price(
            [id], currency), 'BITCOIN:$512,345 ')

        id = 'doge'
        currency = 'usd'
        responses.add(responses.GET,
                      f'{TICKER_API_URL}/simple/price/' +
                      f'?ids={id}&vs_currencies={currency}',
                      json=mock_response(id, currency, 0.223432), status=200)
        self.assertEqual(c.get_latest_price(
            [id], currency), 'DOGE:$0.223432 ')

    @responses.activate
    def test_get_latest_price_error(self):
        responses.add(responses.GET, f'{TICKER_API_URL}/coins/list',
                      json=[{'btc': {'symbol': 'BITCOIN'}}], status=200)
        c = Crypto()
        self.assertRaises(ConnectionError, c.get_latest_price, ['btc'], 'usd')

    @responses.activate
    def test_get_coin(self):
        mock_coin = {'id': 'btc', 'name': 'bitcoin', 'symbol': 'btc'}
        responses.add(responses.GET, f'{TICKER_API_URL}/coins/list',
                      json=[mock_coin], status=200)

        c = Crypto()
        coin = c.get_coin('btc')
        self.assertEqual(coin, mock_coin)

        self.assertRaises(Exception, c.get_coin, 'shitcoin')

    def test_get_logo(self):
        mock_coin = {'id': 'btc', 'name': 'bitcoin', 'symbol': 'btc'}
        location = os.path.dirname(os.path.abspath(__file__)) + \
            '/images/logos/'
        responses.add(responses.GET, f'{TICKER_API_URL}/coins/list',
                      json=[mock_coin], status=200)

        c = Crypto()
        logo = c.get_logo({'symbol':'btc'})
        self.assertEqual(logo, location + 'bitcoin-8px.bmp')
        logo = c.get_logo({'symbol':'btc'})
        self.assertEqual(logo, location + 'ethereum-8px.bmp')
        logo = c.get_logo({'symbol':'btc'})
        self.assertEqual(logo, location + 'dogecoin-8px.bmp')
        logo = c.get_logo({'symbol':'btc'})
        self.assertEqual(logo, None)

        self.assertRaises(Exception, c.get_coin, 'shitcoin')
