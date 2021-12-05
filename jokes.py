import requests

JOKE_API_URL = "https://v2.jokeapi.dev/"


def get_joke():
    """Gets a random joke from the official joke API

    Returns:
        String: The joke
    """
    response = requests.get(build_url())
    response_json = response.json()
    if response_json['type'] == 'twopart':
        return response_json['setup'] + \
            '.....' + response_json['delivery']
    elif response_json['type'] == 'single':
        return response_json['joke']


def build_url():

    return JOKE_API_URL + "joke/Programming,Miscellaneous,Pun,Spooky,Christmas?\
        blacklistFlags=nsfw,racist,sexist,explicit"
