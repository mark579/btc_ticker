import requests

TICKER_API_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_latest_price(id, currency):
    """Gets latest price for a coin vs a currency

    Args:
        id (string): [ID from coingecko API /coins/list]
        currency (string): [Currency from coingecko API /simple/supported_vs_currencies]

    Returns:
        String: [The currenct price]
    """
    response = requests.get(
        f'{TICKER_API_URL}/?ids={id}&vs_currencies={currency}')
    response_json = response.json()
    return "${:,}".format(float(response_json[id][currency])).rstrip('0').rstrip('.')
