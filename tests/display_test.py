from unittest import TestCase
from unittest.mock import patch, MagicMock
import display
import os
import importlib
import time


def mock_text_display(message):
    return f'text(tuple=(0, 0), message={message}, ' \
        + 'fill=white, font=proportional)'


def mock_show_message(message):
    return f'show_message(message={message}, ' \
        + 'fill=white, font=proportional, scroll_delay=0.04)'


class TestDisplay(TestCase):

    def test_sanitize(self):
        message = "Hello this is a simple message"
        self.assertEqual(message, display.Viewer.sanitize(message))

        message = "This message has invalid characters♠★"
        clean_message = "This message has invalid characters"
        self.assertEqual(clean_message, display.Viewer.sanitize(message))

    @patch.dict(os.environ, {"MODE": "CONSOLE"}, clear=True)
    @patch('builtins.print')
    def test_console_mode(self, mock_print):
        # Reload module to pickup mocked environment
        importlib.reload(display)
        # Don't want to wait on sleep in tests
        time.sleep = MagicMock()
        t = display.Viewer()
        self.assertEqual(t.device, 1)

        t.display_message("BIG MONEY", display.MessageType.STATIC)
        mock_print.assert_called_with(mock_text_display("BIG MONEY"))

        t.display_message("BIG MONEY", display.MessageType.SCROLLING)
        mock_print.assert_called_with(mock_show_message("BIG MONEY"))

    @patch.dict(os.environ, {"MODE": "PYGAME"}, clear=True)
    @patch('luma.emulator.device.pygame')
    def test_pygame_mode(self, pygame_mock):
        # Reload module to pickup mocked environment
        importlib.reload(display)
        display.Viewer()
        pygame_mock.assert_called_with(width=64, height=8)
