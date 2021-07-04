import time

from config import Config
from crypto import get_latest_price
from display import Ticker, MessageType
from jokes import get_joke
from requests import ConnectionError


def main():
    ticker = Ticker()
    config = load_config(ticker)
    ticker_display_loop(ticker, config['ticker'])

def load_config(ticker) -> dict:
    try:
        return Config().get_config()
    except FileNotFoundError:
        ticker.display_message(
            f'Config File not found', MessageType.STATIC)
        time.sleep(25)
        main()
    except Exception as e:
        print(e)
        ticker.display_message(f'Unhandled error occured. :(', MessageType.STATIC)
        time.sleep(25)
        main()

def ticker_display_loop(ticker, config):
    i = 0
    message = ""
    routine = ""
    while True:
        i = i+1
        try:
            if(i >= 10 and config['tell_jokes']):
                routine = "Joke"
                message = get_joke()
                ticker.display_message(message, MessageType.SCROLLING)
            else:
                routine = "Price"
                message = get_latest_price(
                    config['crypto'], config['vs_currency'])
                ticker.display_message(message, MessageType.STATIC)
                time.sleep(25)

            if(i >= 10):
                i = 0
        except ConnectionError:
            ticker.display_message(
                f'Error connecting to {routine} API', MessageType.SCROLLING)
        except Exception as e:
            print(e)
            ticker.display_message(
                f'Encounter an Unknown Error', MessageType.SCROLLING)


main()
