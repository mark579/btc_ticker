from unittest import TestCase
from unittest import mock
import config


class TestConfig(TestCase):
    def setUp(self):
        self.mock_config_file = mock.patch.object(
            config, 'CONFIG_FILE', 'tests/test_config.yaml')
        self.missing_config_file = mock.patch.object(
            config, 'CONFIG_FILE', 'tests/nofilehere.yaml')

    def test_config(self):
        with self.mock_config_file:
            c = config.Config().get_config()
            self.assertEqual(c['ticker']['tell_jokes'], False)
            self.assertEqual(c['ticker']['crypto'], 'bitcoin')
            self.assertEqual(c['ticker']['vs_currency'], 'usd')

    def test_missing_config(self):
        with self.missing_config_file:
            self.assertRaises(FileNotFoundError, config.Config)
