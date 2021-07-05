import os
import yaml

CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + '/config.yaml'


class Config:
    def __init__(self) -> None:
        self.config = None
        self.load_config()

    def load_config(self) -> None:
        with open(CONFIG_FILE, 'r') as file:
            self.config = yaml.safe_load(file)
            if(os.environ.get('MODE', None)):
                print(self.config)

    def get_config(self) -> dict:
        return self.config
