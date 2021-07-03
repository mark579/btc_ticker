import time

from display import Ticker, MessageType
from crypto import get_latest_price
from jokes import get_joke
from requests import ConnectionError

ticker = Ticker()


def main():
    i = 0
    message = ""
    routine = ""
    while True:
        i = i+1
        try:
            if(i >= 10):
                routine = "Joke"
                i = 0
                message = get_joke()
                ticker.display_message(message, MessageType.SCROLLING)
            else:
                routine = "Price"
                message = get_latest_price('bitcoin', 'usd')
                ticker.display_message(message, MessageType.STATIC)
                time.sleep(25)
        except ConnectionError:
            ticker.display_message(f'Error connecting to {routine} API', MessageType.SCROLLING)
        except:
            ticker.display_message(f'Encounter an Unknown Error', MessageType.SCROLLING)


main()
