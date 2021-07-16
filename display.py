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

    def sanitize(message) -> str:
        return message.encode("ascii", errors="ignore").decode()

    def display_message(self, message, type):
        """Displays a message based on the MessageType

        Args:
            message (String): The message to display
            type (MessageType): MessageType to display
        """
        font = ImageFont.truetype('./fonts/pixelmix.ttf', 8)
        # message = Viewer.sanitize(message)
        if type == MessageType.STATIC:
            with canvas(self.device) as draw:
                text(draw, (0, 0), message, fill="white",
                     font=proportional(CP437_FONT))
        elif type == MessageType.SCROLLING:
            self.scroll_message(message, font)
        elif type == MessageType.BOUNCING:
            Viewer.bounce_message(self.device, message, x_offset=8, fill="white",
                                  font=font, scroll_delay=0.04, delay=5)

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

    def bounce_message(device, msg, y_offset=0, x_offset=0, fill=None, font=None,
                       scroll_delay=0.03, delay=0):
        fps = 0 if scroll_delay == 0 else 1.0 / scroll_delay
        regulator = framerate_regulator(fps)
        w = font.getsize(msg)[0]

        x = device.width
        virtual = viewport(device, width=w + x, height=device.height)
        virtual.draw_logo = True

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

    def draw_logo(im):
        eraser = Image.new('1', (8, 8))
        im.paste(eraser, (0, 0))
        draw = ImageDraw.Draw(im)
        img = Image.open('./images/logos/bitcoin-8px.bmp')
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

        if hasattr(self, 'draw_logo') and self.draw_logo:
            Viewer.draw_logo(im)
        self._device.display(im)
        del im
