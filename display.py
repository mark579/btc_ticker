from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.interface.serial import noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT

from mocks import mock_setup
spi, max7219, canvas, text, show_message = mock_setup(
    spi, max7219, canvas, text, show_message)

from enum import Enum
class MessageType(Enum):
    STATIC = 1
    SCROLLING = 2

class Ticker:
    def __init__(self) -> None:

        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, cascaded=8, block_orientation=-90,
                         rotate=0, blocks_arranged_in_reverse_order=False)

    def display_message(self, message, type):
        """Displays a message based on the MessageType

        Args:
            message (String): The message to display
            type (MessageType): MessageType to display
        """
        if type == MessageType.STATIC:
            with canvas(self.device) as draw:
                text(draw, (0, 0), message, fill="white",
                    font=proportional(CP437_FONT))
        elif type == MessageType.SCROLLING:
            show_message(self.device, message, fill="white",
                             font=proportional(CP437_FONT), scroll_delay=0.03)