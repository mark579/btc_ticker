from unittest import TestCase
from unittest import mock
import display
import os
import importlib


class TestDisplay(TestCase):
    def test_sanitize(self):
        message = "Hello this is a simple message"
        self.assertEqual(message, display.Ticker.sanitize(message))

        message = "This message has invalid characters♠★"
        clean_message = "This message has invalid characters"
        self.assertEqual(clean_message, display.Ticker.sanitize(message))

    @mock.patch.dict(os.environ, {"MODE": "CONSOLE"}, clear=True)
    def test_init(self):
        # Reload module to pickup mocked environment
        importlib.reload(display)
        t = display.Ticker()
        self.assertEqual(t.device, 1)
