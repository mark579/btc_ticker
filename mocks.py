import os


class mock7219():
    def width():
        return 8


def mock_setup(spi, max7219, canvas):
    """Mocks out methods for easier testing in console

    Args:
        spi ([type]): Global SPI Interface
        max7219 ([type]): Glbal mx7219 Interface
        canvas ([type]): Global canvas
    """
    if (os.environ.get('MODE', None) == "CONSOLE"):
        spi = mock_spi
        max7219 = mock_max7219
        canvas = mock_canvas
    return spi, max7219, canvas


def mock_spi(port=0, device=0, gpio=0):
    return 1


def mock_max7219(serial=0, cascaded=8, block_orientation=-90,
                 rotate=0, blocks_arranged_in_reverse_order=False):
    return mock7219


def mock_canvas(device):
    return MockWith()


class MockWith:
    def __enter__(one):
        return 1

    def __exit__(one, two, three, four):
        return 1
