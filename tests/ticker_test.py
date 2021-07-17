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
            'name': 'Bitcoin', 'id': 'btc', 'symbol': 'btc'}
        mock_logo.return_value = 'bitcoin_file.jpg'
        mock_details.return_value = '$31,000, +10.20%'

        # Don't want to wait on sleep in tests
        time.sleep = mock.MagicMock()
        t = Ticker()
        t.load_config()
        print(t.config)
        t.display_routine()

        calls = [mock.call('Bitcoin', MessageType.FALLING, 'bitcoin_file.jpg')]
        for j in range(0, 3):
            calls.append(mock.call('$31,000, +10.20%', MessageType.BOUNCING,
                                   'bitcoin_file.jpg', delay=30))

        calls.append(mock.call('Joke Time', MessageType.FALLING, delay=25))
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
