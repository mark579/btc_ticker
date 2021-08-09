from crypto import Crypto
from display import MessageType
from requests import ConnectionError
import time
from unittest import TestCase
from unittest import mock
from ticker import Ticker


class TestTicker(TestCase):
    @mock.patch('ticker.Viewer')
    def test_init(self, mock_viewer):
        Ticker()
        mock_viewer.assert_called()

    @mock.patch('ticker.Viewer')
    @mock.patch('ticker.has_internet_connection')
    @mock.patch('ticker.setup_wifi')
    def test_setup_connection(self, setup_wifi, mock_has_internet_connection,
                              mock_viewer):
        mock_has_internet_connection.return_value = True
        t = Ticker()
        t.setup_connection()

        setup_wifi.assert_not_called()

        mock_has_internet_connection.return_value = False
        setup_wifi.return_value = "DID IT BOYS"

        t.setup_connection()
        setup_call = mock.call("SETUP", MessageType.STATIC)
        connect_call = mock.call(
            "Successfully connected to DID IT BOYS", MessageType.SCROLLING)
        t.viewer.display_message.assert_has_calls([setup_call, connect_call])
        setup_wifi.assert_called()

        setup_wifi.side_effect = [Exception(), "DID IT BOYS"]
        t.setup_connection()
        error_call = mock.call("Error connecting to Wi-Fi. Please try again.",
                               MessageType.SCROLLING)
        t.viewer.display_message.assert_has_calls([setup_call, error_call])

    @mock.patch('ticker.Crypto')
    @mock.patch('ticker.Viewer')
    @mock.patch('config.Config.get_config')
    def test_load_config(self, mock_get_config, mock_viewer, mock_crypto):
        # Don't want to wait on sleep in tests
        time.sleep = mock.MagicMock()
        t = Ticker()

        mock_get_config.return_value = "CONFIG!"
        t.load_config()
        self.assertEqual(t.config, 'CONFIG!')

        mock_get_config.side_effect = Exception()
        t.load_config()
        t.viewer.display_message.assert_called_with(
            "Could not load config :(", MessageType.STATIC)

        mock_get_config.side_effect = FileNotFoundError()
        t.load_config()
        t.viewer.display_message.assert_called_with(
            "Config file not found.", MessageType.STATIC)

    @mock.patch('ticker.Crypto.get_logo')
    @mock.patch('ticker.Crypto.get_details')
    @mock.patch('ticker.Crypto.get_coin')
    @mock.patch('ticker.get_joke')
    @mock.patch('ticker.Viewer')
    @mock.patch('config.Config.get_config')
    def test_display_routine(self, mock_get_config, mock_viewer,
                             mock_joke, mock_coin, mock_details, mock_logo):

        mock_get_config.return_value = {'ticker': {
            'tell_jokes': True, 'crypto': 'btc', 'vs_currency': 'usd'}}
        mock_joke.return_value = "FUNNY!"
        mock_coin.return_value = {
            'name': 'Bitcoin',
            'id': 'btc',
            'symbol': 'btc',
            'logo': 'bitcoin_file.jpg'
        }
        mock_logo.return_value = 'bitcoin_file.jpg'
        mock_details.return_value = '$31,000, +10.20%'

        # Don't want to wait on sleep in tests
        time.sleep = mock.MagicMock()
        t = Ticker()
        t.crypto = Crypto()
        t.load_config()
        print(t.config)
        t.display_routine()

        calls = [mock.call('BITCOIN', MessageType.FALLING, 'bitcoin_file.jpg')]
        for j in range(0, 3):
            calls.append(mock.call('$31,000, +10.20%', MessageType.BOUNCING,
                                   'bitcoin_file.jpg', delay=30))

        calls.append(mock.call('JOKE TIME', MessageType.FALLING, delay=25))
        calls.append(mock.call('FUNNY!', MessageType.SCROLLING))

        t.viewer.display_message.assert_has_calls(calls)

        mock_details.side_effect = ConnectionError()
        t.display_routine()
        t.viewer.display_message.assert_called_with(
            "Error connecting to Price API", MessageType.SCROLLING)

        mock_details.side_effect = None
        mock_joke.side_effect = ConnectionError()
        t.display_routine()
        t.viewer.display_message.assert_called_with(
            "Error connecting to Joke API", MessageType.SCROLLING)

        mock_joke.side_effect = Exception()
        t.display_routine()
        t.viewer.display_message.assert_called_with(
            "Encountered an Unknown Error", MessageType.SCROLLING)
