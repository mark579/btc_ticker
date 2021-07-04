import requests
import responses

JOKE_API_URL = "https://official-joke-api.appspot.com/random_joke"


def get_joke():
    """Gets a random joke from the official joke API

    Returns:
        String: The joke
    """
    try:
        response = requests.get(JOKE_API_URL)
        response_json = response.json()
        joke = response_json['setup'] + \
            '.....' + response_json['punchline']
        return joke
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError
