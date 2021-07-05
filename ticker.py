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

    def load_config(self) -> dict:
        try:
            self.config = Config().get_config()
        except FileNotFoundError:
            self.viewer.display_message(
                "Config File not found", MessageType.STATIC)
            time.sleep(25)
        except Exception as e:
            print(e)
            self.viewer.display_message(
                "Unhandled error occured. :(", MessageType.STATIC)
            time.sleep(25)

    def display_loop(self):
        i = 0
        message = ""
        routine = ""
        config = self.config['ticker']
        while True:
            i = i+1
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

                if(i >= 10):
                    i = 0
            except ConnectionError:
                self.viewer.display_message(
                    f'Error connecting to {routine} API',
                    MessageType.SCROLLING)
            except Exception as e:
                print(e)
                self.viewer.display_message(
                    "Encounter an Unknown Error", MessageType.SCROLLING)
