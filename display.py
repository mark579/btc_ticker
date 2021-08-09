from enum import Enum
import os
from luma.led_matrix.device import max7219
# from luma.emulator.device import pygame
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

FONT_FILE = os.path.dirname(os.path.abspath(
    __file__)) + '/fonts/pixelmix_bold.ttf'


class MessageType(Enum):
    STATIC = 1
    SCROLLING = 2
    BOUNCING = 3
    FALLING = 4


class Viewer:
    def __init__(self) -> None:
        self.font = ImageFont.truetype(FONT_FILE, 8)
        viewport.refresh = refresh
        if(os.environ.get('MODE', None) == 'PYGAME'):
            # self.device = pygame(width=64, height=8)
            print("PYGAME NOT SUPPORTED")
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
            self.scroll_message(self.device, message, self.font)
        elif type == MessageType.BOUNCING:
            self.bounce_message(self.device, message,
                                font=self.font, logo=logo, delay=delay)

        elif type == MessageType.FALLING:
            self.drop_message(self.device, message,
                              font=self.font, logo=logo, delay=delay)

    @staticmethod
    def drop_message(device, msg, font=None, logo=None, delay=0):
        x_offset = 0 if logo is None else 8

        regulator = framerate_regulator(10)
        w = font.getsize(msg)[0]

        x = device.width
        virtual = viewport(device, width=w + x, height=device.height+9)
        virtual.logo = logo

        with canvas(virtual) as draw:
            draw.text((x_offset, 0), msg, fill='white', font=font)

        for i in range(9, -1, -1):
            with regulator:
                virtual.set_position((0, i))

        for _ in range(0, delay):
            with regulator:
                virtual.set_position((0, 0))

    @staticmethod
    def scroll_message(device, message, font):
        regulator = framerate_regulator(25)
        x = device.width
        w = font.getsize(message)[0]
        virtual = viewport(device, width=w + x +
                           x, height=device.height)
        with canvas(virtual) as draw:
            draw.text((x, 0), message, fill='white', font=font)

        i = 0
        while i <= w + x:
            with regulator:
                virtual.set_position((i, 0))
                i += 1

    @staticmethod
    def bounce_message(device, msg, font=None, logo=None, delay=0):
        x_offset = 0 if logo is None else 8
        w = font.getsize(msg)[0]
        x = device.width

        regulator = framerate_regulator(20)
        virtual = viewport(device, width=w + x, height=device.height)
        virtual.logo = logo

        with canvas(virtual) as draw:
            draw.text((x_offset, 0), msg, fill='white', font=font)

        i = 0
        for _ in range(0, delay):
            with regulator:
                virtual.set_position((0, 0))

        while i <= w - x:
            with regulator:
                virtual.set_position((i, 0))
                i += 1

        for _ in range(0, delay):
            with regulator:
                virtual.set_position((i, 0))

        while i >= 0:
            with regulator:
                virtual.set_position((i, 0))
                i -= 1
