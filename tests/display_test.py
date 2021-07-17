from unittest import TestCase
from unittest.mock import patch, MagicMock
from mocks import mock7219
import display
import os
import importlib
import time


def mock_display_message(message, type):
    return f'display_message(message:{message}, ' + \
        f'type:{type}, logo:None, delay:15'


class TestDisplay(TestCase):
    @ patch.dict(os.environ, {"MODE": "CONSOLE"}, clear=True)
    @ patch('builtins.print')
    def test_console_mode(self, mock_print):
        # Reload module to pickup mocked environment
        importlib.reload(display)
        # Don't want to wait on sleep in tests
        time.sleep = MagicMock()
        t = display.Viewer()
        self.assertEqual(t.device, mock7219)

        t.display_message("BIG MONEY", display.MessageType.STATIC)
        mock_print.assert_called_with(
            mock_display_message("BIG MONEY",
                                 display.MessageType.STATIC))

        t.display_message("BIG MONEY", display.MessageType.SCROLLING)
        mock_print.assert_called_with(
            mock_display_message("BIG MONEY",
                                 display.MessageType.SCROLLING))

    @ patch.dict(os.environ, {"MODE": "PYGAME"}, clear=True)
    @ patch('luma.emulator.device.pygame')
    def test_pygame_mode(self, pygame_mock):
        # Reload module to pickup mocked environment
        importlib.reload(display)
        display.Viewer()
        pygame_mock.assert_called_with(width=64, height=8)
