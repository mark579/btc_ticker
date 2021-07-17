from enum import Enum
import os
from luma.led_matrix.device import max7219
from luma.emulator.device import pygame
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT
from luma.core.sprite_system import framerate_regulator
from luma.core.virtual import viewport
from luma.core.virtual import hotspot
from luma.core.threadpool import threadpool
from PIL import Image, ImageDraw, ImageFont


from mocks import mock_setup
spi, max7219, canvas, text, show_message = mock_setup(
    spi, max7219, canvas, text, show_message)

pool = threadpool(4)


class MessageType(Enum):
    STATIC = 1
    SCROLLING = 2
    BOUNCING = 3
    FALLING = 4


class Viewer:
    def __init__(self) -> None:
        viewport.refresh = Viewer.monkey_patch_refresh
        if(os.environ.get('MODE', None) == 'PYGAME'):
            self.device = pygame(width=64, height=8)
        else:
            serial = spi(port=0, device=0, gpio=noop())
            self.device = max7219(serial, cascaded=8, block_orientation=-90,
                                  rotate=0,
                                  blocks_arranged_in_reverse_order=False)

    def display_message(self, message, type, logo=None):
        """Displays a message based on the MessageType

        Args:
            message (String): The message to display
            type (MessageType): MessageType to display
        """
        font = ImageFont.truetype('./fonts/pixelmix_bold.ttf', 8)
        if type == MessageType.STATIC:
            with canvas(self.device) as draw:
                text(draw, (0, 0), message, fill="white",
                     font=proportional(CP437_FONT))
        elif type == MessageType.SCROLLING:
            self.scroll_message(message, font)
        elif type == MessageType.BOUNCING:
            # If logo offset
            Viewer.bounce_message(self.device, message, logo=logo,
                                  fill="white", font=font,
                                  scroll_delay=0.05, delay=30)

        elif type == MessageType.FALLING:
            # If logo offset
            Viewer.drop_message(self.device, message, font=font, logo=logo, delay=15)

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
        fps = 1.0 / 0.04
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

    def bounce_message(device, msg, y_offset=0, logo=None, fill=None, font=None,
                       scroll_delay=0.03, delay=0):
        fps = 0 if scroll_delay == 0 else 1.0 / scroll_delay
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

    def draw_logo(im, logo_file):
        eraser = Image.new('1', (8, 8))
        im.paste(eraser, (0, 0))
        draw = ImageDraw.Draw(im)
        img = Image.open(logo_file)
        draw.bitmap((0, 1), img, fill='white')

    def monkey_patch_refresh(self):
        should_wait = False
        for hotspot, xy in self._hotspots:
            if hotspot.should_redraw() and self.is_overlapping_viewport(hotspot, xy):
                pool.add_task(hotspot.paste_into, self._backing_image, xy)
                should_wait = True

        if should_wait:
            pool.wait_completion()

        im = self._backing_image.crop(box=self._crop_box())
        if self._dither:
            im = im.convert(self._device.mode)

        if hasattr(self, 'logo') and self.logo:
            Viewer.draw_logo(im, self.logo)
        self._device.display(im)
        del im
