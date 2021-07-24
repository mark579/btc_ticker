import subprocess
import urllib
import requests

from crypto import TICKER_API_URL


def has_internet_connection():

    # Check if we can contact API
    try:
        output = subprocess.run(['nmcli', '-t', 'g'], capture_output=True)
        print(str(output.stdout))
        if ('full' not in str(output.stdout)):
            return(False)
        urllib.request.urlopen(TICKER_API_URL + '/ping')
        return(True)
    except Exception:
        print('EXCEPTION LOADING API URL')
        return(False)


def setup_wifi():
    subprocess.run(['wifi-connect'], capture_output=True)
    wifi = subprocess.run(['wifi-connect', '-r'], capture_output=True)
    return (str(wifi.stdout))
