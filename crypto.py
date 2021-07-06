import requests

TICKER_API_URL = "https://api.coingecko.com/api/v3"


class Crypto:
    def __init__(self):
        self.coins = Crypto.coins_request()

    def get_coin(self, id):
        for coin in self.coins:
            if coin['id'] == id:
                return coin
        raise Exception('Coin not found in coin list.')

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
            prices += f'{str.upper(coin["symbol"])}: {price} '

        return(prices)

    def price_request(ids, currency):
        return requests.get(
            f'{TICKER_API_URL}/simple/price/?ids=' +
            f'{",".join(ids)}&vs_currencies={currency}').json()

    def coins_request():
        return requests.get(
            f'{TICKER_API_URL}/coins/list').json()
