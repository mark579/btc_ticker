from enum import Enum
import os
from luma.led_matrix.device import max7219
from luma.emulator.device import pygame
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT
from luma.core.sprite_system import framerate_regulator
from luma.core.virtual import viewport
from viewport_patch import refresh
from PIL import ImageFont


from mocks import mock_setup
spi, max7219, canvas = mock_setup(
    spi, max7219, canvas)


class MessageType(Enum):
    STATIC = 1
    SCROLLING = 2
    BOUNCING = 3
    FALLING = 4


class Viewer:
    def __init__(self) -> None:
        self.font = ImageFont.truetype('./fonts/pixelmix_bold.ttf', 8)
        viewport.refresh = refresh
        if(os.environ.get('MODE', None) == 'PYGAME'):
            self.device = pygame(width=64, height=8)
        else:
            serial = spi(port=0, device=0, gpio=noop())
            self.device = max7219(serial, cascaded=8, block_orientation=-90,
                                  rotate=0,
                                  blocks_arranged_in_reverse_order=False)

    def display_message(self, message, type, logo=None, delay=15):
        """Displays a message based on the MessageType

        Args:
            message (String): The message to display
            type (MessageType): MessageType to display
        """
        if(os.environ.get('MODE', None) == 'CONSOLE'):
            print(f'display_message(message:{message}, type:{type}' +
                  f', logo:{logo}, delay:{delay}')
            return

        if type == MessageType.STATIC:
            with canvas(self.device) as draw:
                text(draw, (0, 0), message, fill="white",
                     font=proportional(CP437_FONT))
        elif type == MessageType.SCROLLING:
            self.scroll_message(message, self.font)
        elif type == MessageType.BOUNCING:
            Viewer.bounce_message(self.device, message, logo=logo,
                                  font=self.font, delay=delay)

        elif type == MessageType.FALLING:
            Viewer.drop_message(self.device, message,
                                font=self.font, logo=logo, delay=delay)

    def drop_message(device, msg, font=None, logo=None, delay=0):
        fps = 10
        x_offset = 0
        if logo is not None:
            x_offset = 8

        regulator = framerate_regulator(fps)
        w = font.getsize(msg)[0]

        x = device.width
        virtual = viewport(device, width=w + x, height=device.height+9)
        virtual.logo = logo

        with canvas(virtual) as draw:
            draw.text((x_offset, 0), msg, fill='white', font=font)

        i = 9
        j = 0
        while i >= 0:
            with regulator:
                virtual.set_position((0, i))
                i -= 1

        while j <= delay:
            with regulator:
                virtual.set_position((0, 0))
                j += 1

    def scroll_message(self, message, font):
        fps = 25
        regulator = framerate_regulator(fps)
        x = self.device.width
        w = font.getsize(message)[0]
        virtual = viewport(self.device, width=w + x +
                           x, height=self.device.height)
        with canvas(virtual) as draw:
            draw.text((x, 0), message, fill='white', font=font)

        i = 0
        while i <= w + x:
            with regulator:
                virtual.set_position((i, 0))
                i += 1

    def bounce_message(device, msg, y_offset=0, logo=None, font=None,
                       delay=0):
        fps = 20
        regulator = framerate_regulator(fps)
        w = font.getsize(msg)[0]

        x_offset = 0
        if logo is not None:
            x_offset = 8

        x = device.width
        virtual = viewport(device, width=w + x, height=device.height)
        virtual.logo = logo

        with canvas(virtual) as draw:
            draw.text((x_offset, y_offset), msg, fill='white', font=font)

        i = 0
        j = 0
        while j <= delay:
            with regulator:
                virtual.set_position((0, 0))
                j += 1

        while i <= w - x:
            with regulator:
                virtual.set_position((i, 0))
                i += 1

        while j >= 0:
            with regulator:
                virtual.set_position((i, 0))
                j -= 1

        while i >= 0:
            with regulator:
                virtual.set_position((i, 0))
                i -= 1
