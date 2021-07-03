import time
import os

def mock_setup(spi, max7219, canvas, text, show_messsage):
    """Mocks out methods for easier testing in console

    Args:
        spi ([type]): Global SPI Interface
        max7219 ([type]): Glbal mx7219 Interface
        canvas ([type]): Global canvas
        text ([type]): Global text display method
        show_messsage ([type]): Global show_message method
    """
    if (os.environ.get('DEV', None)):
        spi = mock_spi
        max7219 = mock_max7219
        canvas = mock_canvas
        text = mock_text
        show_message = mock_show_message
    return spi, max7219, canvas, text, show_message


def mock_spi(port=0, device=0, gpio=0):
    return 1

def mock_max7219(serial=0, cascaded=8, block_orientation=-90,rotate=0, blocks_arranged_in_reverse_order=False):
    return 1

def mock_canvas(device):
    return MockWith()

def mock_text(draw, tuple, message, fill="white", font="MOCK"):
    print(f'text(tuple={tuple}, message={message}, fill={fill}, font={type(font).__name__})')
    return 1

def mock_show_message(device, message, fill, font, scroll_delay):
    print(f'show_message(message={message}, fill={fill}, font={type(font).__name__}, scroll_delay={scroll_delay})')
    time.sleep(1/scroll_delay)

    return 1

class MockWith:
    def __enter__(one): 
        return 1
    def __exit__(one, two, three, four):
        return 1
