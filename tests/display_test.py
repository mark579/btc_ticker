from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from PIL import ImageFont
from mocks import mock7219
import display
import os
import importlib
import time

test7219 = mock7219()


def mock_display_message(message, type):
    return f'display_message(message:{message}, ' + \
        f'type:{type}, logo:None, delay:15'


class TestDisplay(TestCase):
    @patch.dict(os.environ, {"MODE": "CONSOLE"}, clear=True)
    @patch('builtins.print')
    def test_console_mode(self, mock_print):
        # Reload module to pickup mocked environment
        importlib.reload(display)
        # Don't want to wait on sleep in tests
        time.sleep = MagicMock()
        t = display.Viewer()
        self.assertIsInstance(t.device, mock7219)

        t.display_message("BIG MONEY", display.MessageType.STATIC)
        mock_print.assert_called_with(
            mock_display_message("BIG MONEY",
                                 display.MessageType.STATIC))

        t.display_message("BIG MONEY", display.MessageType.SCROLLING)
        mock_print.assert_called_with(
            mock_display_message("BIG MONEY",
                                 display.MessageType.SCROLLING))

    @patch.dict(os.environ, {"MODE": "PYGAME"}, clear=True)
    @patch('luma.emulator.device.pygame')
    def test_pygame_mode(self, pygame_mock):
        # Reload module to pickup mocked environment
        importlib.reload(display)
        display.Viewer()
        pygame_mock.assert_called_with(width=64, height=8)

    @patch('display.framerate_regulator')
    @patch('display.viewport')
    @patch('display.canvas')
    def test_drop_message(self, mock_canvas, mock_viewport, mock_regulator):
        canvas = MagicMock()
        draw = MagicMock()
        canvas.__enter__ = MagicMock(return_value=draw)
        virtual = MagicMock()
        regulator = MagicMock()
        mock_regulator.return_value = regulator
        mock_viewport.return_value = virtual
        mock_canvas.return_value = canvas
        font = ImageFont.truetype('./fonts/pixelmix_bold.ttf', 8)
        display.Viewer.drop_message(test7219, 'TEST',
                                    font=font, logo=None, delay=0)

        mock_regulator.assert_called_with(10)
        mock_canvas.assert_called_with(virtual)
        draw.text.assert_called_with((0, 0), 'TEST', fill='white', font=font)

        calls = []
        for i in range(9, -1, -1):
            calls.append(call((0, i)))

        virtual.set_position.assert_has_calls(calls)

        display.Viewer.drop_message(test7219, 'TEST',
                                    font=font, logo='logo.bmp', delay=0)

        # Has 8px offset when logos is added
        draw.text.assert_called_with((8, 0), 'TEST', fill='white', font=font)

    @patch('display.framerate_regulator')
    @patch('display.viewport')
    @patch('display.canvas')
    def test_scroll_message(self, mock_canvas, mock_viewport, mock_regulator):
        canvas = MagicMock()
        draw = MagicMock()
        canvas.__enter__ = MagicMock(return_value=draw)
        virtual = MagicMock()
        regulator = MagicMock()
        mock_regulator.return_value = regulator
        mock_viewport.return_value = virtual
        mock_canvas.return_value = canvas
        font = ImageFont.truetype('./fonts/pixelmix_bold.ttf', 8)
        display.Viewer.scroll_message(test7219, 'TEST',
                                      font=font)

        mock_regulator.assert_called_with(25)
        mock_canvas.assert_called_with(virtual)
        draw.text.assert_called_with(
            (mock7219.width, 0), 'TEST', fill='white', font=font)
        w = font.getsize('TEST')[0]
        calls = []
        for i in range(0, w + mock7219.width):
            calls.append(call((i, 0)))

        virtual.set_position.assert_has_calls(calls)

    @patch('display.framerate_regulator')
    @patch('display.viewport')
    @patch('display.canvas')
    def test_bounce_message(self, mock_canvas, mock_viewport, mock_regulator):
        canvas = MagicMock()
        draw = MagicMock()
        canvas.__enter__ = MagicMock(return_value=draw)
        virtual = MagicMock()
        regulator = MagicMock()
        mock_regulator.return_value = regulator
        mock_viewport.return_value = virtual
        mock_canvas.return_value = canvas
        test_txt = 'BOUNCY MESSAGE'
        font = ImageFont.truetype('./fonts/pixelmix_bold.ttf', 8)
        display.Viewer.bounce_message(test7219, test_txt,
                                      font=font, logo=None, delay=0)

        mock_regulator.assert_called_with(20)
        mock_canvas.assert_called_with(virtual)
        draw.text.assert_called_with((0, 0), test_txt,
                                     fill='white', font=font)

        w = font.getsize(test_txt)[0]
        x = mock7219.width

        calls = []
        i = 0
        while i <= w - x:
            calls.append(call((i, 0)))
            i += 1

        while i >= 0:
            calls.append(call((i, 0)))
            i -= 1

        virtual.set_position.assert_has_calls(calls)

        display.Viewer.bounce_message(test7219, test_txt,
                                      font=font, logo='logo.bmp', delay=0)

        # Has 8px offset when logos is added
        draw.text.assert_called_with((8, 0), test_txt,
                                     fill='white', font=font)
