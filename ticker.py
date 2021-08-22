import time
from config import Config
from crypto import Crypto
from display import Viewer, MessageType
from jokes import get_joke
from requests import ConnectionError
from wifi import has_internet_connection, setup_wifi


class Ticker():
    def __init__(self) -> None:
        self.viewer = Viewer()
        self.config = None
        self.crypto = None

    def start(self):
        self.setup_connection()
        while(self.config is None):
            self.load_config()
        self.crypto = Crypto()
        self.display_loop()

    def setup_connection(self):
        if not has_internet_connection():
            try:
                self.viewer.display_message(
                    "SETUP", MessageType.STATIC)
                wifi = setup_wifi()
                if(len(wifi) > 0):
                    self.viewer.display_message(
                        f'Successfully connected to {wifi}',
                        MessageType.SCROLLING)
            except Exception:
                self.viewer.display_message(
                    "Error connecting to Wi-Fi. Please try again.",
                    MessageType.SCROLLING)
                self.setup_connection()

    def display_loop(self):
        while True:
            self.load_config()
            self.display_routine()

    def display_routine(self):
        routine = ""
        config = self.config['ticker']
        try:
            routine = "Price"
            for crypto in config['crypto']:
                coin = self.crypto.get_coin(crypto)
                self.viewer.display_message(str.upper(coin["name"]),
                                            MessageType.FALLING, coin['logo'])
                for j in range(0, 3):
                    message = self.crypto.get_details(
                        crypto, config['vs_currency'])
                    self.viewer.display_message(message,
                                                MessageType.BOUNCING,
                                                coin['logo'],
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
                "Config not found.", MessageType.SCROLLING)
            time.sleep(25)
        except Exception as e:
            print(e)
            self.viewer.display_message(
                "Could not load config, contact support",
                MessageType.SCROLLING)
