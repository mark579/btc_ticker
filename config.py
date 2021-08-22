import os
import json
import requests
import uuid

CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + '/config.json'
CONFIG_HOST_URL = os.environ.get('CONFIG_URL', 'http://localhost:8080')


class Config:
    def __init__(self) -> None:
        self.config = None
        self.load_config()

    def load_config(self):
        if(os.environ.get('CONFIG', None) == 'local'):
            self.load_local_config()
        else:
            self.load_remote_config()

        if(os.environ.get('MODE', None)):
            print(self.config)

    def load_local_config(self) -> None:
        with open(CONFIG_FILE, 'r') as file:
            self.config = json.load(file)

    def load_remote_config(self) -> None:
        config_url = f'{CONFIG_HOST_URL}/config?UUID={Config.uuid()}'
        response = requests.get(config_url)
        if(response.status_code == 200):
            config = response.json()
            self.config = config
        else:
            if(response.status_code == 404):
                raise Exception('Server does not know of config')
            else:
                raise Exception('Error loading config from Server')

    def uuid():
        mac = hex(uuid.getnode())
        urn = f'urn:node:{mac}'
        return uuid.uuid3(uuid.NAMESPACE_DNS, urn)

    def get_config(self) -> dict:
        return self.config
