import subprocess
import urllib
import os
from crypto import TICKER_API_URL


def has_internet_connection():
    if os.environ.get('SKIP_INTERNET_CHECK', False) == '1':
        return True

    try:
        output = subprocess.run(['nmcli', '-t', 'g'], capture_output=True)
        if ('full' not in str(output.stdout)):
            return (False)
        urllib.request.urlopen(TICKER_API_URL + '/ping')
        return (True)
    except Exception:
        return (False)


def setup_wifi():
    subprocess.run(['sudo', 'wifi-connect', '--portal-ssid',
                    'MAD_Crypto_Ticker'], capture_output=True)
    wifi = subprocess.run(['iwgetid', '-r'], capture_output=True)
    return (wifi.stdout.decode('utf-8').rstrip())
