import os
from requests import get

TICKER_API_URL = "https://api.coingecko.com/api/v3"
IMAGE_LOCATION = os.path.dirname(os.path.abspath(__file__)) + '/images/logos/'


class Crypto:
    def __init__(self):
        self.coins = Crypto.coins_request()

    def get_coin(self, id):
        for coin in self.coins:
            if coin['id'] == id:
                coin['logo'] = self.get_logo(coin)
                return coin
        raise Exception('Coin not found in coin list.')

    def get_logo(self, coin):
        if(coin['symbol'] == 'btc'):
            return IMAGE_LOCATION + 'bitcoin-8px.bmp'
        if(coin['symbol'] == 'eth'):
            return IMAGE_LOCATION + 'ethereum-8px.bmp'
        if(coin['symbol'] == 'doge'):
            return IMAGE_LOCATION + 'dogecoin-8px.bmp'
        return None

    def get_latest_price(self, ids, currency):
        """Gets latest price for a coin vs a currency

        Args:
            ids (Array(string)): IDs from coingecko API /coins/list
            currency (string): Currency from coingecko API
                                /simple/supported_vs_currencies

        Returns:
            str: Formatted string of all prcies in format ID: Price
            e.g. BITCOIN: $35,000 DOGECOIN: $0.2500
        """
        prices = ''
        response = Crypto.price_request(ids, currency)
        for id in ids:
            price = "${:,}".format(float(response[id][currency]))
            price = price.rstrip('0').rstrip('.')
            coin = self.get_coin(id)
            prices += f'{str.upper(coin["symbol"])}:{price} '

        return(prices)

    def get_details(self, id, currency):
        response = Crypto.markets_request(id, currency)
        price = "${:,}".format(float(response[0]['current_price']))
        percent_change = "{0:.2f}%".format(
            float(response[0]['price_change_percentage_24h']))
        return f'{price} {percent_change}%'

    def price_request(ids, currency):
        return get(
            f'{TICKER_API_URL}/simple/price/?ids=' +
            f'{",".join(ids)}&vs_currencies={currency}').json()

    def markets_request(id, currency):
        return get(
            f'{TICKER_API_URL}/coins/markets?vs_currency={currency}' +
            f'&ids={id}').json()

    def coins_request():
        return get(
            f'{TICKER_API_URL}/coins/list').json()
