from requests import ConnectionError
from unittest import TestCase
from unittest import mock
import wifi
import os


class TestWifi(TestCase):
    @mock.patch("wifi.subprocess.run")
    @mock.patch("wifi.urllib.request.urlopen")
    def test_has_internet_connection(self, urlopen, run):
        run.return_value = "EMPTY"
        status = wifi.has_internet_connection()
        run.assert_called_with(['nmcli', '-t', 'g'],
                               capture_output=True)
        self.assertEqual(status, False)

        output = mock.MagicMock()
        output.stdout = "full"
        run.return_value = output
        status = wifi.has_internet_connection()
        urlopen.return_value = "yep"
        self.assertEqual(status, True)

        urlopen.side_effect = ConnectionError()
        status = wifi.has_internet_connection()
        self.assertEqual(status, False)

    @mock.patch.dict(os.environ, {"SKIP_INTERNET_CHECK": "1"}, clear=True)
    def test_skip_connection(self):
        status = wifi.has_internet_connection()
        self.assertEqual(status, True)

    @mock.patch("wifi.subprocess.run")
    def test_setup_wifi(self, run):
        output = mock.MagicMock()
        output.stdout = b"M@DSUNSHINECREATIONS"
        run.return_value = output
        wifi_name = wifi.setup_wifi()
        run.assert_has_calls([mock.call(['sudo', 'wifi-connect',
                                         '--portal-ssid',
                                         'MAD_Crypto_Ticker'],
                                        capture_output=True),
                              mock.call(['iwgetid', '-r'],
                              capture_output=True)])
        self.assertEqual(wifi_name, "M@DSUNSHINECREATIONS")
