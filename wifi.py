import subprocess
import urllib
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
    output = subprocess.run(['sudo', 'wifi-connect', '--portal-ssid', 'MAD_Crypto_Ticker'], capture_output=True)
    print('Tried to run wifi-connect')
    print(str(output.stdout))
    wifi = subprocess.run(['iwgetid', '-r'], capture_output=True)
    return (wifi.stdout.decode('utf-8').rstrip())
