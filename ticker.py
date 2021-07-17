import time
from config import Config
from crypto import Crypto
from display import Viewer, MessageType
from jokes import get_joke
from requests import ConnectionError


class Ticker():
    def __init__(self) -> None:
        self.viewer = Viewer()
        self.config = None
        self.crypto = Crypto()

    def start(self):
        while(self.config is None):
            self.load_config()

        self.display_loop()

    def display_loop(self):
        while True:
            self.display_routine()

    def display_routine(self):
        routine = ""
        config = self.config['ticker']
        try:
            routine = "Price"
            for crypto in config['crypto']:
                coin = self.crypto.get_coin(crypto)
                logo = self.crypto.get_logo(coin)
                self.viewer.display_message(str.upper(coin["name"]),
                                            MessageType.FALLING, logo)
                for j in range(0, 3):
                    message = self.crypto.get_details(
                        crypto, config['vs_currency'])
                    self.viewer.display_message(message,
                                                MessageType.BOUNCING, logo,
                                                delay=30)

            if(config['tell_jokes']):
                routine = "Joke"
                message = get_joke()
                self.viewer.display_message("JOKE TIME", MessageType.FALLING,
                                            delay=25)
                self.viewer.display_message(message, MessageType.SCROLLING)
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
