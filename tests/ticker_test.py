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
    @mock.patch('config.Config.get_config')
    def test_load_config(self, mock_get_config, mock_viewer):
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

    @mock.patch('ticker.get_joke')
    @mock.patch('ticker.Crypto.get_latest_price')
    @mock.patch('ticker.Viewer')
    @mock.patch('config.Config.get_config')
    def test_display_routine(self, mock_get_config, mock_viewer,
                             mock_latest_price, mock_joke):
        mock_get_config.return_value = {'ticker': {
            'tell_jokes': True, 'crypto': 'btc', 'vs_currency': 'usd'}}
        mock_latest_price.return_value = "$100,000"
        mock_joke.return_value = "FUNNY!"
        # Don't want to wait on sleep in tests
        time.sleep = mock.MagicMock()
        t = Ticker()
        t.load_config()
        print(t.config)
        t.display_routine(1)
        t.viewer.display_message.assert_called_with(
            "$100,000", MessageType.SCROLLING)

        t.display_routine(10)
        t.viewer.display_message.assert_called_with(
            "FUNNY!", MessageType.SCROLLING)

        mock_latest_price.side_effect = ConnectionError()
        t.display_routine(1)
        t.viewer.display_message.assert_called_with(
            "Error connecting to Price API", MessageType.SCROLLING)

        mock_joke.side_effect = ConnectionError()
        t.display_routine(10)
        t.viewer.display_message.assert_called_with(
            "Error connecting to Joke API", MessageType.SCROLLING)

        mock_joke.side_effect = Exception()
        t.display_routine(10)
        t.viewer.display_message.assert_called_with(
            "Encountered an Unknown Error", MessageType.SCROLLING)
