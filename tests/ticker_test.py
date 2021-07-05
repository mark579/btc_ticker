import display
from unittest import TestCase
from unittest import mock
from ticker import Ticker


class TestTicker(TestCase):
    @mock.patch('ticker.Viewer')
    def test_init(self, mock_viewer):
        display.Viewer = mock.MagicMock()
        Ticker()
        mock_viewer.assert_called()
