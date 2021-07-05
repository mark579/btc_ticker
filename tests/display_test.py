from unittest import TestCase
from unittest.mock import patch, MagicMock
import display
import os
import importlib
import time


class TestDisplay(TestCase):
    def test_sanitize(self):
        message = "Hello this is a simple message"
        self.assertEqual(message, display.Ticker.sanitize(message))

        message = "This message has invalid characters♠★"
        clean_message = "This message has invalid characters"
        self.assertEqual(clean_message, display.Ticker.sanitize(message))

    @patch.dict(os.environ, {"MODE": "CONSOLE"}, clear=True)
    @patch('builtins.print')
    def test_console_mode(self, mock_print):
        # Reload module to pickup mocked environment
        importlib.reload(display)
        # Don't want to wait on sleep in tests
        time.sleep = MagicMock()
        t = display.Ticker()
        self.assertEqual(t.device, 1)

        t.display_message("BIG MONEY", display.MessageType.STATIC)
        mock_print.assert_called_with(
            'text(tuple=(0, 0), message=BIG MONEY, \
                fill=white, font=proportional)')

        t.display_message("BIG MONEY", display.MessageType.SCROLLING)
        mock_print.assert_called_with(
            'show_message(message=BIG MONEY, \
                fill=white, font=proportional, scroll_delay=0.03)')

    @patch.dict(os.environ, {"MODE": "PYGAME"}, clear=True)
    def test_pygame_mode(self):
        # Reload module to pickup mocked environment
        importlib.reload(display)
        t = display.Ticker()
        self.assertEqual(type(t.device).__name__, 'pygame')
