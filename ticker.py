import time
from config import Config
from crypto import get_latest_price
from display import Viewer, MessageType
from jokes import get_joke
from requests import ConnectionError


class Ticker():
    def __init__(self) -> None:
        self.viewer = Viewer()
        self.config = None

    def start(self):
        while(self.config is None):
            self.load_config()

        self.display_loop()

    def display_loop(self):
        i = 0
        while True:
            i = i+1
            self.display_routine(i)
            if(i >= 10):
                i = 0

    def display_routine(self, i):
        routine = ""
        config = self.config['ticker']
        try:
            if(i >= 10 and config['tell_jokes']):
                routine = "Joke"
                message = get_joke()
                self.viewer.display_message(message, MessageType.SCROLLING)
            else:
                routine = "Price"
                message = get_latest_price(
                    config['crypto'], config['vs_currency'])
                self.viewer.display_message(message, MessageType.STATIC)
                time.sleep(25)
        except ConnectionError:
            self.viewer.display_message(
                f'Error connecting to {routine} API',
                MessageType.SCROLLING)
        except Exception as e:
            print(e)
            self.viewer.display_message(
                "Encountered an Unknown Error", MessageType.SCROLLING)

    def load_config(self) -> dict:
        try:
            self.config = Config().get_config()
        except FileNotFoundError:
            self.viewer.display_message(
                "Config file not found.", MessageType.STATIC)
            time.sleep(25)
        except Exception as e:
            print(e)
            self.viewer.display_message(
                "Could not load config :(", MessageType.STATIC)
            time.sleep(25)
