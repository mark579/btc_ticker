import time

def mock_spi(port=0, device=0, gpio=0):
    return 1

def mock_max7219(serial=0, cascaded=8, block_orientation=-90,rotate=0, blocks_arranged_in_reverse_order=False):
    return 1

def mock_canvas(device):
    return MockWith()

def mock_text(draw, tuple, message, fill="white", font="MOCK"):
    print(message)
    return 1

def mock_show_message(device, message, fill, font, scroll_delay):
    print(message)
    time.sleep(1/scroll_delay)

    return 1

class MockWith:
    def __enter__(one): 
        return 1
    def __exit__(one, two, three, four):
        return 1
